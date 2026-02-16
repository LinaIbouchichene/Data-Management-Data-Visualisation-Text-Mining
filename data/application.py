# ======================================================
# ACCIDENTS EXPLORER — VERSION FINALE OPTIMISÉE
# ======================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------------------------------
# BRANDING — Inspired by Les Echos
# -----------------------------------------------------
BRAND_PRIMARY = "#B21807"
BRAND_SECONDARY = "#63150C"
BRAND_ACCENT = "#D9B28C"
BRAND_DARK = "#1F1F1F"
BRAND_LIGHT = "#F7F3EE"
BRAND_NEUTRAL = "#D9D4CE"
BRAND_CHART_SEQUENCE = [
    "#B21807",
    "#D94F30",
    "#E88A64",
    "#5C5C5C",
]
BRAND_BAR_SEQUENCE = [
    "#B21807",
    "#C53020",
    "#D94F30",
    "#E47354",
    "#EF9B79",
    "#F3B892",
    "#7E2B18",
    "#A64E3D",
    "#CC6E58",
    "#F7D6C2",
]
NAV_FLOW = {
    "home": {"next": "dataset"},
    "dataset": {"prev": "home", "next": "viz"},
    "viz": {"prev": "dataset", "next": "article"},
    "article": {"prev": "viz"},
}
BAAC_SCHEMA_PATH = Path("assets/baac_schema.png")
ARTICLE_WORDCLOUD_PATH = Path("assets/article_wordcloud.png")
ARTICLE_PATH = Path("article.txt")

# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------
st.set_page_config(page_title="Observatoire des accidents de la route", layout="wide")


# -----------------------------------------------------
# LOAD DATA (FINAL_2023)
# -----------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("clean/final_2023.csv")

    # Fix longitude naming
    df = df.rename(columns={
        "long": "longitude",
        "lon": "longitude",
        "lng": "longitude",
        "Long": "longitude"
    })

    # Fix sexe label
    df["sexe"] = pd.to_numeric(df["sexe"], errors="coerce").astype("Int64")
    df["sexe_label"] = df["sexe"].map({1: "Homme", 2: "Femme"})

    return df


df = load_data()


def inject_branding():
    css = f"""
    <style>
    :root {{
        --brand-primary: {BRAND_PRIMARY};
        --brand-secondary: {BRAND_SECONDARY};
        --brand-accent: {BRAND_ACCENT};
        --brand-dark: {BRAND_DARK};
        --brand-light: {BRAND_LIGHT};
    }}
    .stApp {{
        background: {BRAND_LIGHT};
        color: {BRAND_DARK};
        font-family: 'Georgia', 'Times New Roman', serif;
    }}
    div.block-container {{
        max-width: 1200px;
        padding-top: 2rem;
    }}
    h1, h2, h3, h4 {{
        color: {BRAND_DARK};
        font-family: 'Playfair Display', 'Georgia', serif;
    }}
    .stButton button {{
        background: {BRAND_PRIMARY};
        color: white;
        border-radius: 999px;
        padding: 0.4rem 1.5rem;
        border: none;
        font-weight: 600;
        box-shadow: none;
    }}
    .stButton button:hover {{
        background: {BRAND_SECONDARY};
        color: #fff;
    }}
    .metric-container, .stMetric {{
        background: #fff;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 1px solid {BRAND_NEUTRAL};
    }}
    .le-table-wrapper {{
        background: #fff;
        border: 1px solid {BRAND_NEUTRAL};
        border-radius: 6px;
        padding: 0.5rem 0.5rem 0.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
        overflow-x: auto;
    }}
    .le-table-wrapper.scrollable {{
        max-height: 320px;
        overflow-y: auto;
    }}
    table.le-table {{
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.95rem;
        color: {BRAND_DARK};
    }}
    table.le-table thead th {{
        background: {BRAND_PRIMARY};
        color: white;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-size: 0.8rem;
        padding: 0.6rem;
    }}
    table.le-table tbody td {{
        border-bottom: 1px solid {BRAND_NEUTRAL};
        padding: 0.55rem 0.6rem;
    }}
    table.le-table tbody tr:nth-child(even) {{
        background: {BRAND_LIGHT};
    }}
    table.le-table tbody tr:hover {{
        background: #fdfbf8;
    }}
    .nav-arrow {{
        position: fixed;
        top: 50%;
        transform: translateY(-50%);
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: {BRAND_PRIMARY};
        color: #fff !important;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.18);
        z-index: 1000;
        transition: background 0.2s ease, transform 0.2s ease;
    }}
    .nav-arrow.nav-arrow-left {{
        left: 1.2rem;
    }}
    .nav-arrow.nav-arrow-right {{
        right: 1.2rem;
    }}
    .nav-arrow:hover {{
        background: {BRAND_SECONDARY};
        transform: translateY(-50%) scale(1.05);
    }}
    .hero-container {{
        max-width: 800px;
        margin: 4rem auto 3rem;
        background: #fff;
        padding: 2.5rem 3rem;
        border-radius: 10px;
        border: 1px solid {BRAND_NEUTRAL};
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.08);
        text-align: center;
    }}
    .hero-container h1 {{
        font-size: 2.8rem;
        margin-bottom: 1rem;
    }}
    .hero-container p {{
        font-size: 1.05rem;
        line-height: 1.7;
        margin-bottom: 1rem;
        color: {BRAND_DARK};
    }}
    .baac-card {{
        background: #fff;
        border: 1px solid {BRAND_NEUTRAL};
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 16px 35px rgba(0, 0, 0, 0.05);
    }}
    .baac-card h3 {{
        font-size: 1.4rem;
        margin-bottom: 0.6rem;
    }}
    .baac-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1rem;
    }}
    .baac-section {{
        background: {BRAND_LIGHT};
        border-radius: 8px;
        padding: 0.8rem;
        border: 1px solid {BRAND_NEUTRAL};
    }}
    .baac-section h4 {{
        margin: 0 0 0.4rem;
        font-size: 1rem;
    }}
    .baac-section ul {{
        padding-left: 1.2rem;
        margin: 0;
    }}
    .baac-section li {{
        font-size: 0.95rem;
        margin-bottom: 0.2rem;
    }}
    .prep-card {{
        background: #fff;
        border: 1px solid {BRAND_NEUTRAL};
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 16px 35px rgba(0, 0, 0, 0.05);
    }}
    .prep-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap: 1rem;
    }}
    .prep-section {{
        background: {BRAND_LIGHT};
        border-radius: 8px;
        padding: 0.9rem;
        border: 1px solid {BRAND_NEUTRAL};
    }}
    .prep-section h4 {{
        margin: 0 0 0.4rem;
        font-size: 1rem;
    }}
    .prep-section ul {{
        padding-left: 1.1rem;
        margin: 0;
    }}
    .prep-section li {{
        font-size: 0.95rem;
        margin-bottom: 0.2rem;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_table(dataframe, *, index=False, scroll=False, height=320):
    df_display = dataframe.copy()
    if not index:
        df_display = df_display.reset_index(drop=True)
    df_display = df_display.fillna("")
    html = df_display.to_html(index=index, classes="le-table", border=0, escape=False)
    wrapper_classes = ["le-table-wrapper"]
    style_attr = ""
    if scroll:
        wrapper_classes.append("scrollable")
        if height:
            style_attr = f"style='max-height:{height}px'"
    class_attr = " ".join(wrapper_classes)
    st.markdown(f"<div class='{class_attr}' {style_attr}>{html}</div>", unsafe_allow_html=True)


def style_plot(fig):
    fig.update_layout(
        template="simple_white",
        title_text="",
        legend_title_text="",
        font=dict(family="Georgia, 'Times New Roman', serif", color=BRAND_DARK, size=14),
        title_font=dict(size=24, family="Playfair Display, Georgia, serif", color=BRAND_DARK),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        bargap=0.2,
        margin=dict(t=60, b=40, l=40, r=30),
    )
    fig.update_xaxes(showgrid=False, linecolor=BRAND_NEUTRAL)
    fig.update_yaxes(showgrid=True, gridcolor="#EFE8E1", zerolinecolor="#EFE8E1")
    fig.update_layout(coloraxis_colorbar=dict(title=""))
    return fig


def bar_colors(count):
    seq = []
    palette = BRAND_BAR_SEQUENCE
    for i in range(count):
        seq.append(palette[i % len(palette)])
    return seq


def render_baac_overview():
    st.subheader("Bulletin d'analyse des accidents corporels (BAAC)")
    st.markdown(
        """
        <div class="baac-card">
            <p>Chaque ligne du dataset est issue du bulletin BAAC qui décrit précisément un accident corporel. Le formulaire est structuré en plusieurs volets :</p>
            <div class="baac-grid">
                <div class="baac-section">
                    <h4>Caractéristiques</h4>
                    <ul>
                        <li>Date, heure, luminosité et météo</li>
                        <li>Localisation détaillée et type d’intersection</li>
                        <li>Type de collision et situation de l’accident</li>
                    </ul>
                </div>
                <div class="baac-section">
                    <h4>Lieux</h4>
                    <ul>
                        <li>Catégorie de route, voie spéciale et aménagement</li>
                        <li>Régime de circulation et état de surface</li>
                        <li>Facteurs liés au lieu (travaux, obstacle, profil)</li>
                    </ul>
                </div>
                <div class="baac-section">
                    <h4>Véhicules</h4>
                    <ul>
                        <li>Type de véhicule et usage (transport, Deux-Roues, PL...)</li>
                        <li>Facteurs liés au véhicule ou au conducteur</li>
                        <li>Trajectoire, point de choc initial, équipement, assurance</li>
                    </ul>
                </div>
                <div class="baac-section">
                    <h4>Usagers</h4>
                    <ul>
                        <li>Catégorie d’usager et place dans le véhicule</li>
                        <li>Âge, sexe, gravité, équipement de sécurité</li>
                        <li>Trajet, action au moment du choc, circonstances particulières</li>
                    </ul>
                </div>
            </div>
            <p style="margin-top:1rem;">Ces rubriques sont transformées en variables dans le fichier <code>final_2023.csv</code>, ce qui permet d’expliquer chaque indicateur affiché sur les pages suivantes.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if BAAC_SCHEMA_PATH.exists():
        st.image(str(BAAC_SCHEMA_PATH), caption="Schéma BAAC officiel (source ONISR)", use_container_width=True)
    else:
        st.caption("Ajoutez un visuel du formulaire BAAC dans assets/baac_schema.png pour l'afficher ici.")


def render_preparation_overview():
    st.subheader("Pipeline de préparation des données")
    st.markdown(
        """
        <div class="prep-card">
            <p>Les quatre tables brutes de la BAAC (caractéristiques, lieux, usagers, véhicules) ont été diagnostiquées puis nettoyées avant fusion. Les principales actions réalisées sont résumées ci-dessous :</p>
            <div class="prep-grid">
                <div class="prep-section">
                    <h4>Caractéristiques</h4>
                    <ul>
                        <li>Contrôle de l’identifiant Num_Acc et recherche de doublons.</li>
                        <li>Nettoyage des coordonnées GPS (remplacement virgules/points) et conversion des colonnes numériques.</li>
                        <li>Détection des valeurs incohérentes (jour/mois/heure) via les bornes BAAC.</li>
                    </ul>
                </div>
                <div class="prep-section">
                    <h4>Lieux</h4>
                    <ul>
                        <li>Remplacement des champs vides par NaN et typage numérique.</li>
                        <li>Filtrage des codes hors plage pour catr, profil, surface, situation, vma.</li>
                        <li>Suppression des variables peu renseignées ou textuelles (voie, pr, plan…).</li>
                    </ul>
                </div>
                <div class="prep-section">
                    <h4>Usagers</h4>
                    <ul>
                        <li>Harmonisation des identifiants usagers/véhicules pour les jointures.</li>
                        <li>Neutralisation des valeurs aberrantes (sexe, gravité, trajet, localisation piéton...).</li>
                        <li>Retrait des colonnes spécifiques et très incomplètes (secu1-3, locp, actp, etatp).</li>
                    </ul>
                </div>
                <div class="prep-section">
                    <h4>Véhicules</h4>
                    <ul>
                        <li>Nettoyage de l’identifiant véhicule et suppression des codes fantômes.</li>
                        <li>Contrôle des catégories (catv, motorisation, manœuvres) via les tables BAAC.</li>
                        <li>Suppression des colonnes peu utiles (motor, obs, manv, occutc).</li>
                    </ul>
                </div>
            </div>
            <p style="margin-top:1rem;">Après fusion, plusieurs variables dérivées ont été créées pour faciliter l’analyse : période de la journée (à partir de <code>hrmn</code>), niveau de gravité simplifié (<code>grav_3_niveaux</code>), tranches d’âge (<code>tranche_age</code>), contexte de zone (<code>zone_detaillee</code>) et niveaux de vitesse (<code>niveau_vitesse</code>). Toutes ces transformations sont documentées dans le notebook de préparation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_viz_filters(dataframe):
    """Render dynamic filters and return the filtered dataframe used in the viz page."""
    st.markdown("### Filtres dynamiques")
    st.caption("Affinez les visualisations en sélectionnant les profils d'usagers à comparer.")

    filtered = dataframe.copy()
    base = dataframe.copy()
    col1, col2, col3 = st.columns(3)

    sexe_options = sorted(base["sexe_label"].dropna().unique().tolist())
    selected_sexes = col1.multiselect(
        "Sexe de l'usager",
        options=sexe_options,
        default=sexe_options,
        placeholder="Tous les sexes",
    )
    if selected_sexes:
        filtered = filtered[filtered["sexe_label"].isin(selected_sexes)]

    grav_order = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
    grav_options = [label for label in grav_order if label in base["grav_3_niveaux"].dropna().unique().tolist()]
    selected_grav = col2.multiselect(
        "Gravité déclarée",
        options=grav_options,
        default=grav_options,
        placeholder="Toutes les gravités",
    )
    if selected_grav:
        filtered = filtered[filtered["grav_3_niveaux"].isin(selected_grav)]

    zone_options = sorted(base["zone_detaillee"].dropna().unique().tolist())
    selected_zones = col3.multiselect(
        "Zone de circulation",
        options=zone_options,
        default=zone_options,
        placeholder="Toutes les zones",
    )
    if selected_zones:
        filtered = filtered[filtered["zone_detaillee"].isin(selected_zones)]

    age_series = base["age"].dropna()
    if not age_series.empty:
        min_age = int(age_series.min())
        max_age = int(age_series.max())
        age_min, age_max = st.slider(
            "Âge des usagers",
            min_value=min_age,
            max_value=max_age,
            value=(min_age, max_age),
            step=1,
        )
        filtered = filtered[filtered["age"].between(age_min, age_max)]

    col_flag1, col_flag2 = st.columns(2)
    night_only = col_flag1.checkbox("Limiter aux accidents de nuit", value=False)
    if night_only:
        filtered = filtered[filtered["periode"] == "Nuit"]

    severe_only = col_flag2.checkbox(
        "Focaliser sur les accidents graves",
        value=False,
        help="Tués ou blessés hospitalisés",
    )
    if severe_only:
        filtered = filtered[filtered["grav_3_niveaux"].isin(["Tué", "Blessé hospitalisé"])]

    st.caption(
        f"{len(filtered):,}".replace(",", " ")
        + f" usagers sélectionnés sur {len(dataframe):,}".replace(",", " ")
    )

    return filtered


inject_branding()


# -----------------------------------------------------
# PAGE : Dataset
# -----------------------------------------------------
def page_dataset(df):

    st.title("Présentation du Dataset")

    col1, col2, col3 = st.columns(3)
    col1.metric("Nombre d'accidents", len(df))
    col2.metric("Année", "2023")
    col3.metric("Variables", df.shape[1])

    render_baac_overview()
    render_preparation_overview()

    st.subheader("Types des variables")
    types_df = (
        df.dtypes.astype(str)
        .reset_index()
        .rename(columns={"index": "Variable", 0: "Type"})
    )
    render_table(types_df, index=False, scroll=True, height=280)

    st.subheader("Valeurs manquantes (%)")
    missing_df = (
        (df.isna().mean() * 100)
        .round(2)
        .reset_index()
        .rename(columns={"index": "Variable", 0: "Valeurs manquantes (%)"})
    )
    fig_missing = px.bar(
        missing_df,
        y="Variable",
        x="Valeurs manquantes (%)",
        orientation="h",
        color_discrete_sequence=[BRAND_PRIMARY],
    )
    fig_missing = style_plot(fig_missing)
    fig_missing.update_layout(xaxis_title="%", yaxis_title="")
    st.plotly_chart(fig_missing, use_container_width=True)

    st.subheader("Aperçu du dataset")
    render_table(df.head(), index=False, scroll=True, height=260)

    st.subheader("Statistiques descriptives")
    stats_df = (
        df.describe(include="all")
        .transpose()
        .reset_index()
        .rename(columns={"index": "Variable"})
    )
    render_table(stats_df, index=False, scroll=True, height=320)


# -----------------------------------------------------
# PAGE : Visualisations
# -----------------------------------------------------
def page_viz(df):

    st.title("Visualisations interactives (2023)")
    st.caption("Ces graphiques décrivent l'ensemble des usagers impliqués dans un accident corporel (conducteurs, passagers, piétons), qu'ils soient responsables ou victimes.")

    # ------------------------------
    # ÉCHANTILLONNAGE AUTOMATIQUE
    # ------------------------------
    dff = df.copy()
    if len(dff) > 30000:
        dff = dff.sample(30000, random_state=42)

    dff = apply_viz_filters(dff)
    if dff.empty:
        st.warning("Aucun enregistrement ne correspond à ces critères. Ajustez les filtres pour poursuivre l'analyse.")
        return

    st.markdown(
        "### Introduction\nLa majorité des usagers impliqués ressortent indemnes ou avec des blessures légères, "
        "et l'on constate que les hommes apparaissent près de deux fois plus souvent que les femmes dans les accidents."
    )
    col_grav, col_sexe = st.columns(2)
    with col_grav:
        st.subheader("Gravité des accidents")
        grav_data = dff.dropna(subset=["grav_3_niveaux"])
        fig_grav = px.pie(
            grav_data,
            names="grav_3_niveaux",
            color_discrete_sequence=BRAND_CHART_SEQUENCE,
        )
        fig_grav = style_plot(fig_grav)
        fig_grav.update_traces(textposition="inside", hole=0.15)
        st.plotly_chart(fig_grav, use_container_width=True)

    with col_sexe:
        st.subheader("Implication par sexe")
        involvement = (
            dff.dropna(subset=["sexe_label"])
            .groupby("sexe_label")
            .size()
            .reset_index(name="accidents")
        )
        fig_invol = px.pie(
            involvement,
            names="sexe_label",
            values="accidents",
            color="sexe_label",
            color_discrete_sequence=BRAND_CHART_SEQUENCE[:2],
        )
        fig_invol = style_plot(fig_invol)
        fig_invol.update_traces(textposition="inside", hole=0.2)
        st.plotly_chart(fig_invol, use_container_width=True)

    st.markdown(
        "### Gravité selon le sexe\nMême si les hommes sont plus nombreux au volant, la répartition des niveaux de gravité "
        "reste proche de celle des femmes : les deux genres subissent proportionnellement autant d'accidents graves quand ils sont impliqués."
    )
    sexe_counts = (
        dff.dropna(subset=["sexe_label", "grav_3_niveaux"])
        .groupby(["sexe_label", "grav_3_niveaux"])
        .size()
        .reset_index(name="accidents")
    )
    sexe_share = sexe_counts.assign(
        part=lambda x: x["accidents"] / x.groupby("sexe_label")["accidents"].transform("sum")
    )
    fig_sexe = px.bar(
        sexe_share,
        x="sexe_label",
        y="part",
        color="grav_3_niveaux",
        barmode="group",
        color_discrete_sequence=BRAND_CHART_SEQUENCE,
    )
    fig_sexe = style_plot(fig_sexe)
    fig_sexe.update_layout(
        xaxis_title="Sexe",
        yaxis_title="Part des accidents",
        legend_title_text="Gravité",
    )
    fig_sexe.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig_sexe, use_container_width=True)

    st.markdown(
        "### Dynamiques d'âge\nLes accidents impliquent surtout les 25–59 ans, mais lorsqu'on observe la part d'accidents nocturnes, "
        "les mineurs se démarquent largement : la conduite nocturne représente un risque particulier pour les plus jeunes."
    )
    age_order = ["Mineur", "18–24", "25–39", "40–59", "60+"]
    col_age, col_night = st.columns(2)
    with col_age:
        st.subheader("Répartition par tranche d'âge")
        age_data = (
            dff.dropna(subset=["tranche_age", "grav_3_niveaux"])
            .assign(tranche_age=lambda x: pd.Categorical(x["tranche_age"], categories=age_order, ordered=True))
        )
        age_counts = (
            age_data.groupby(["tranche_age", "grav_3_niveaux"], observed=False)
            .size()
            .reset_index(name="accidents")
            .sort_values("tranche_age")
        )
        fig_age = px.bar(
            age_counts,
            x="tranche_age",
            y="accidents",
            color="grav_3_niveaux",
            barmode="stack",
            color_discrete_sequence=BRAND_CHART_SEQUENCE,
        )
        fig_age = style_plot(fig_age)
        fig_age.update_layout(
            xaxis_title="Tranches d'âge",
            yaxis_title="Nombre d'accidents",
            legend_title_text="Gravité",
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with col_night:
        st.subheader("Part de la nuit par tranche d'âge")
        night_data = (
            dff.dropna(subset=["periode", "tranche_age"])
            .assign(tranche_age=lambda x: pd.Categorical(x["tranche_age"], categories=age_order, ordered=True))
        )
        # Ensure every paire (tranche_age, période) exists so percentages remain correct even after filtering.
        nuit_index = pd.MultiIndex.from_product(
            [age_order, ["Matin", "Après-midi", "Soir", "Nuit"]],
            names=["tranche_age", "periode"],
        )
        night_counts = (
            night_data.groupby(["tranche_age", "periode"], observed=False)
            .size()
            .reindex(nuit_index, fill_value=0)
            .reset_index(name="accidents")
        )
        total_by_age = night_counts.groupby("tranche_age")["accidents"].sum().reset_index(name="total")
        night_share = (
            night_counts.merge(total_by_age, on="tranche_age")
            .assign(part=lambda x: x["accidents"] / x["total"])
            .pipe(lambda df: df[df["periode"] == "Nuit"])
            .sort_values("part", ascending=False)
        )
        fig_night = px.bar(
            night_share,
            x="tranche_age",
            y="part",
            color="tranche_age",
            color_discrete_sequence=BRAND_BAR_SEQUENCE,
        )
        fig_night = style_plot(fig_night)
        fig_night.update_layout(
            xaxis_title="Tranches d'âge",
            yaxis_title="Part des accidents sur la période Nuit",
            showlegend=False,
        )
        fig_night.update_yaxes(tickformat=".0%")
        st.plotly_chart(fig_night, use_container_width=True)

    st.subheader("Accidents par période et zone de circulation")
    periode_data = (
        dff.dropna(subset=["periode", "zone_detaillee"])
        .assign(periode=lambda x: pd.Categorical(x["periode"], categories=["Matin", "Après-midi", "Soir", "Nuit"], ordered=True))
    )
    zone_categories = sorted(periode_data["zone_detaillee"].unique().tolist())
    periode_index = pd.MultiIndex.from_product(
        [["Matin", "Après-midi", "Soir", "Nuit"], zone_categories or ["Zone inconnue"]],
        names=["periode", "zone_detaillee"],
    )
    periode_counts = (
        periode_data.groupby(["periode", "zone_detaillee"], observed=False)
        .size()
        .reindex(periode_index, fill_value=0)
        .reset_index(name="accidents")
        .sort_values("periode")
    )
    if not zone_categories:
        periode_counts = periode_counts[periode_counts["zone_detaillee"] == "Zone inconnue"]
    fig_periode = px.bar(
        periode_counts,
        x="periode",
        y="accidents",
        color="zone_detaillee",
        color_discrete_sequence=BRAND_BAR_SEQUENCE,
    )
    fig_periode = style_plot(fig_periode)
    fig_periode.update_layout(
        xaxis_title="Période",
        yaxis_title="Nombre d'accidents",
        legend_title_text="Zone détaillée",
    )
    st.plotly_chart(fig_periode, use_container_width=True)

    st.markdown(
        "### Gravité par environnement\nLes espaces ruraux ou périurbains concentrent une part plus élevée d'accidents graves. "
        "Le treemap permet d'identifier les environnements où la mortalité ou les blessures lourdes sont proportionnellement les plus présentes."
    )
    zone_data = dff.dropna(subset=["zone_detaillee", "grav_3_niveaux"])
    zone_summary = (
        zone_data.assign(grave=lambda x: x["grav_3_niveaux"].isin(["Tué", "Blessé hospitalisé"]).astype(int))
        .groupby("zone_detaillee", observed=False)
        .agg(total=("grav_3_niveaux", "size"), graves=("grave", "sum"))
        .reset_index()
        .assign(part_graves=lambda x: x["graves"] / x["total"])
    )
    fig_zone = px.treemap(
        zone_summary,
        path=["zone_detaillee"],
        values="total",
        color="part_graves",
        color_continuous_scale=[BRAND_LIGHT, BRAND_PRIMARY],
        color_continuous_midpoint=zone_summary["part_graves"].mean(),
    )
    fig_zone.update_layout(
        margin=dict(t=50, l=0, r=0, b=0),
        coloraxis_colorbar=dict(title="Part d'accidents graves", tickformat=".0%"),
    )
    st.plotly_chart(fig_zone, use_container_width=True)

    st.markdown(
        "### Gravité et vitesse\nPlus la limitation est élevée, plus la part d'accidents graves augmente — un rappel direct "
        "que les initiatives plaidant pour moins de signalisation ou un code de la route « plus léger » risquent d'amplifier les conséquences physiques."
    )
    speed_data = (
        dff.dropna(subset=["niveau_vitesse", "grav_3_niveaux"])
        .assign(grave=lambda x: x["grav_3_niveaux"].isin(["Tué", "Blessé hospitalisé"]).astype(int))
    )
    speed_summary = (
        speed_data.groupby("niveau_vitesse", observed=False)
        .agg(total=("grav_3_niveaux", "size"), graves=("grave", "sum"))
        .reset_index()
        .assign(part_graves=lambda x: x["graves"] / x["total"])
    )
    vitesse_order = ["Faible", "Moyenne", "Élevée"]
    speed_summary["niveau_vitesse"] = pd.Categorical(speed_summary["niveau_vitesse"], categories=vitesse_order, ordered=True)
    speed_summary = speed_summary.sort_values("niveau_vitesse")
    fig_speed = px.line(
        speed_summary,
        x="niveau_vitesse",
        y="part_graves",
        markers=True,
        color_discrete_sequence=[BRAND_PRIMARY],
    )
    fig_speed = style_plot(fig_speed)
    fig_speed.update_layout(
        xaxis_title="Niveau de vitesse autorisée",
        yaxis_title="Part d'accidents graves",
        showlegend=False,
    )
    fig_speed.update_yaxes(tickformat=".0%")
    st.plotly_chart(fig_speed, use_container_width=True)


# -----------------------------------------------------
# NAVIGATION HELPERS
# -----------------------------------------------------
def _normalize_param(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value


def resolve_stage():
    qp = st.query_params
    param_stage = _normalize_param(qp.get("stage"))
    if param_stage in NAV_FLOW:
        stage = param_stage
    else:
        stage = st.session_state.get("stage", "home")
    if stage not in NAV_FLOW:
        stage = "home"
    st.session_state.stage = stage
    if _normalize_param(st.query_params.get("stage")) != stage:
        st.query_params["stage"] = stage
    return stage


def stage_link(target_stage):
    return f"?stage={target_stage}"


def render_navigation_arrows(stage):
    flow = NAV_FLOW.get(stage, {})
    html_parts = []
    prev_stage = flow.get("prev")
    next_stage = flow.get("next")
    if prev_stage:
        html_parts.append(
            f"<a class='nav-arrow nav-arrow-left' title='Étape précédente' href='{stage_link(prev_stage)}' target='_self'>&#8592;</a>"
        )
    if next_stage:
        html_parts.append(
            f"<a class='nav-arrow nav-arrow-right' title='Étape suivante' href='{stage_link(next_stage)}' target='_self'>&#8594;</a>"
        )
    if html_parts:
        st.markdown("".join(html_parts), unsafe_allow_html=True)


def render_home():
    st.markdown(
        """
        <div class="hero-container">
            <h1>Observatoire des accidents de la route</h1>
            <p>L’Observatoire des accidents de la route est une application interactive développée avec Streamlit, dédiée à l’analyse des accidents de la route en France en 2023 à partir des données officielles de la Base des Accidents Corporels (BAAC).</p>
            <p>L’application propose une exploration progressive en plusieurs étapes : une présentation détaillée du jeu de données (structure, types de variables, valeurs manquantes, statistiques descriptives), suivie de visualisations interactives permettant d’analyser les profils des usagers, les périodes à risque, les tranches d’âge et la gravité des accidents.</p>
            <p>Conçue dans une logique de data management et de data visualisation, elle vise à rendre un jeu de données volumineux et complexe plus lisible, tout en mettant en évidence les principaux enjeux de sécurité routière à travers des indicateurs clairs et des graphiques interactifs.</p>
            <p style="margin-top:1.5rem;font-weight:600;">Utilisez la flèche à droite pour parcourir les sections.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_dataset():
    st.markdown("### Étape 1 · Dataset")
    st.write("Faites défiler librement, la flèche à droite reste accessible pour passer aux visualisations.")
    page_dataset(df)


def render_viz():
    st.markdown("### Étape 2 · Visualisations")
    page_viz(df)

def render_article():
    st.markdown("### Étape 3 · Article et analyse textuelle")
    st.write("Nuage de mots extrait de l'article de presse récent et accès direct au contenu.")

    if ARTICLE_WORDCLOUD_PATH.exists():
        st.image(str(ARTICLE_WORDCLOUD_PATH), caption="Nuage de mots — Sécurité routière 2023", use_container_width=True)
    else:
        st.warning("Aucun nuage de mots généré. Ajoutez assets/article_wordcloud.png pour l'afficher.")

    st.link_button(
        "Consulter l'article du Monde",
        "https://www.lemonde.fr/societe/article/2024/02/01/securite-routiere-en-2023-le-nombre-de-morts-sur-les-routes-de-france-en-baisse-par-rapport-a-2022_6213781_3224.html",
        help="Ouvre l'article complet dans votre navigateur."
    )

    if ARTICLE_PATH.exists():
        st.download_button(
            "Télécharger l'article (texte)",
            ARTICLE_PATH.read_text(),
            file_name="article_securite_routiere_2023.txt",
            mime="text/plain"
        )
    else:
        st.warning("Le fichier article.txt est introuvable dans le dossier du projet.")


# -----------------------------------------------------
# MAIN
# -----------------------------------------------------
def main():

    stage = resolve_stage()
    render_navigation_arrows(stage)

    if stage == "home":
        render_home()
    elif stage == "dataset":
        render_dataset()
    elif stage == "viz":
        render_viz()
    else:
        render_article()


# -----------------------------------------------------
# START
# -----------------------------------------------------
main()
