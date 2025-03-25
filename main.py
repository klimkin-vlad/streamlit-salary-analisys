import pandas as pd
import streamlit as st

st.header("Анализ роста зарплат")

st.write("Данные")

salaries_new = pd.read_excel("tab3_zpl_2023.xlsx", index_col = 0, sheet_name = 0, header = 4)
salaries_old = pd.read_excel("tab3_zpl_2023.xlsx", index_col = 0, sheet_name = 1, header = 2)
salaries_new_sel = salaries_new.iloc[[17, 43, 50]]
salaries_old_sel = salaries_old.iloc[[10, 28, 32]]
salaries_new_sel = salaries_new_sel.rename(index = {"    производство одежды": "Одежда", "деятельность в области информации и связи": "Связь", "образование": "Образование"})
salaries_old_sel = salaries_old_sel.rename(index = {"  текстильное и швейное производство": "Одежда", "     из них связь": "Связь", "Образование": "Образование"})

st.table(salaries_new_sel)
st.table(salaries_old_sel)

salaries = pd.concat([salaries_old_sel, salaries_new_sel], axis = 1).T
st.table(salaries)

st.write("График зарплат")
st.line_chart(salaries)

st.write("Сравнение зарплат с учётом инфляции и без неё")

inflation = pd.read_html("Таблицы уровня инфляции.html", index_col = 0)
inflation_sel = pd.Series(inflation[0]["Всего"], index = inflation[0].index).iloc[1:25]
inflation_sel[2000] = 0
inflation_year = pd.DataFrame({"Год": 1 + inflation_sel / 100, "Инфляция": pd.NA})
inflation_year = inflation_year.loc[::-1]
inflation_year["Инфляция"][2000] = 100
inflation_year["Инфляция"] = inflation_year["Год"].cumprod()

salaries_inflation = pd.concat([salaries, inflation_year], axis = 1)
salaries_inflation["Одежда (инфляция)"] = salaries_inflation["Одежда"] / salaries_inflation["Инфляция"]
salaries_inflation["Связь (инфляция)"] = salaries_inflation["Связь"] / salaries_inflation["Инфляция"]
salaries_inflation["Образование (инфляция)"] = salaries_inflation["Образование"] / salaries_inflation["Инфляция"]

st.table(salaries_inflation)

st.write("График зарплат с учётом инфляции")
st.line_chart(salaries_inflation[["Одежда (инфляция)", "Связь (инфляция)", "Образование (инфляция)"]])
