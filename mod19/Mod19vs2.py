import pandas            as pd
import streamlit         as st
import seaborn           as sns
import matplotlib.pyplot as plt
from PIL import Image
from io                  import BytesIO

# Ajuste de estilo Seaborn
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

# ===================== FUNÇÕES =====================

@st.cache_data(show_spinner=True)
def load_data(file_data):
    try:
        return pd.read_csv(file_data, sep=';')
    except:
        return pd.read_excel(file_data)

@st.cache_data
def multiselect_filter(relatorio, col, selecionados):
    if 'all' in selecionados:
        return relatorio
    else:
        return relatorio[relatorio[col].isin(selecionados)].reset_index(drop=True)

@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

@st.cache_resource
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

# ===================== APP PRINCIPAL =====================

def main():
    st.set_page_config(
        page_title="Telemarketing Analysis",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("📞 Telemarketing Analysis")
    st.markdown("---")

    # Imagem na sidebar
try:
    image = Image.open("mod19/img/Bank-Branding.jpg")
    st.sidebar.image(image, use_column_width=True)
except:
    st.sidebar.warning("Imagem não encontrada em 'mod19/img/Bank-Branding.jpg'")

    st.sidebar.write("## Suba o arquivo")
    data_file_1 = st.sidebar.file_uploader("Bank marketing data", type=['csv', 'xlsx'])

    if data_file_1 is not None:
        bank_raw = load_data(data_file_1)
        bank = bank_raw.copy()

        st.write("## Antes dos filtros")
        st.write(bank_raw.head())

        with st.sidebar.form(key='my_form'):
            graph_type = st.radio("Tipo de gráfico:", ("Barras", "Pizza"))

            max_age = int(bank.age.max())
            min_age = int(bank.age.min())
            idades = st.slider("Idade", min_value=min_age, max_value=max_age, value=(min_age, max_age), step=1)

            jobs_list = bank.job.unique().tolist()
            jobs_list.append('all')
            jobs_selected = st.multiselect("Profissão", jobs_list, ['all'])

            marital_list = bank.marital.unique().tolist()
            marital_list.append('all')
            marital_selected = st.multiselect("Estado civil", marital_list, ['all'])

            default_list = bank.default.unique().tolist()
            default_list.append('all')
            default_selected = st.multiselect("Default", default_list, ['all'])

            housing_list = bank.housing.unique().tolist()
            housing_list.append('all')
            housing_selected = st.multiselect("Tem financiamento imob?", housing_list, ['all'])

            loan_list = bank.loan.unique().tolist()
            loan_list.append('all')
            loan_selected = st.multiselect("Tem empréstimo?", loan_list, ['all'])

            contact_list = bank.contact.unique().tolist()
            contact_list.append('all')
            contact_selected = st.multiselect("Meio de contato", contact_list, ['all'])

            month_list = bank.month.unique().tolist()
            month_list.append('all')
            month_selected = st.multiselect("Mês do contato", month_list, ['all'])

            day_of_week_list = bank.day_of_week.unique().tolist()
            day_of_week_list.append('all')
            day_of_week_selected = st.multiselect("Dia da semana", day_of_week_list, ['all'])

            bank = (bank.query("age >= @idades[0] and age <= @idades[1]")
                        .pipe(multiselect_filter, 'job', jobs_selected)
                        .pipe(multiselect_filter, 'marital', marital_selected)
                        .pipe(multiselect_filter, 'default', default_selected)
                        .pipe(multiselect_filter, 'housing', housing_selected)
                        .pipe(multiselect_filter, 'loan', loan_selected)
                        .pipe(multiselect_filter, 'contact', contact_selected)
                        .pipe(multiselect_filter, 'month', month_selected)
                        .pipe(multiselect_filter, 'day_of_week', day_of_week_selected))

            submit_button = st.form_submit_button(label='Aplicar')

        st.write("## Após os filtros")
        st.write(bank.head())

        df_xlsx = to_excel(bank)
        st.download_button("📥 Download tabela filtrada em EXCEL", data=df_xlsx, file_name="bank_filtered.xlsx")

    # Proporção de resposta positiva
        if bank_raw is not None and bank is not None:
            try:
                if 'y' in bank_raw.columns and 'y' in bank.columns and not bank_raw.empty and not bank.empty:
                    bank_raw_target_perc = bank_raw['y'].value_counts(normalize=True).rename_axis('y').reset_index(name='percent')
                    bank_raw_target_perc['percent'] *= 100

                    bank_target_perc = bank['y'].value_counts(normalize=True).rename_axis('y').reset_index(name='percent')
                    bank_target_perc['percent'] *= 100

                    col1, col2 = st.columns(2)
                    col1.write("### Proporção original")
                    col1.dataframe(bank_raw_target_perc)
                    col1.download_button("📥 Download", data=to_excel(bank_raw_target_perc), file_name="bank_raw_y.xlsx")

                    col2.write("### Proporção da tabela com filtros")
                    col2.dataframe(bank_target_perc)
                    col2.download_button("📥 Download", data=to_excel(bank_target_perc), file_name="bank_y.xlsx")

                    st.markdown("---")
                    st.write("## Proporção de aceite")

                    fig, ax = plt.subplots(1, 2, figsize=(10, 5))

                    if graph_type == "Barras":
                        sns.barplot(x='y', y='percent', data=bank_raw_target_perc, ax=ax[0])
                        ax[0].bar_label(ax[0].containers[0])
                        ax[0].set_title("Dados brutos", fontweight="bold")

                        sns.barplot(x='y', y='percent', data=bank_target_perc, ax=ax[1])
                        ax[1].bar_label(ax[1].containers[0])
                        ax[1].set_title("Dados filtrados", fontweight="bold")
                    else:
                        ax[0].pie(bank_raw_target_perc['percent'], labels=bank_raw_target_perc['y'], autopct='%.2f%%')
                        ax[0].set_title("Dados brutos", fontweight="bold")

                        ax[1].pie(bank_target_perc['percent'], labels=bank_target_perc['y'], autopct='%.2f%%')
                        ax[1].set_title("Dados filtrados", fontweight="bold")

                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.warning("Os dados não possuem a coluna 'y' ou estão vazios. Verifique os filtros aplicados.")

            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar os gráficos: {e}")
        else:
            st.info("Por favor, envie um arquivo CSV ou XLSX para iniciar.")

# Final da função main
if __name__ == '__main__':
    main()
