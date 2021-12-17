import streamlit as st
from multipage import MultiPage
from pages import home
from pages import tiempos
from pages import mapas

app = MultiPage()

app.add_page("..."                         , home.app     )
app.add_page("Me mudo / Cambio de trabajo" , tiempos.app  )
app.add_page("Tráfico ladrón de tiempo"    , mapas.app    )

app.run()