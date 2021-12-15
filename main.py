import streamlit as st
from multipage import MultiPage
from pages import home
from pages import org_dest
from pages import tiempos
from pages import mapas

app = MultiPage()

app.add_page("Index"                , home.app     )
app.add_page("Origen-Destino"       , org_dest.app )
app.add_page("Tiempos desde origen" , tiempos.app  )
app.add_page("Mapas"                , mapas.app    )

app.run()