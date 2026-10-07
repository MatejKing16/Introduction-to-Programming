"""
Firemní informační a účetní systém pro správu akcí (EventCorp ERP).
Tento modul zpracovává kalkulaci nákladů koncertu na Letné, analýzu rizik počasí
a poskytuje grafické rozhraní (UI) s přihlášením a tiskem účetního PDF.
"""

from __future__ import annotations

import datetime
import math
import os
import sys
import tkinter as tk
from dataclasses import dataclass
from tkinter import filedialog, messagebox, ttk

# Import knihovny ReportLab pro tisk účetních PDF dokumentů
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


# ==============================================================================
# 1. DATOVÁ VRSTVA A MODELY (Data Types & Structures)
# ==============================================================================

class ExpenseItem:
    """Datová reprezentace jedné nákladové položky."""

    def __init__(self, nazev: str, kategorie: str, pocet: str, cena_kc: float):
        self.nazev = nazev
        self.kategorie = kategorie
        self.pocet = pocet
        self.cena_kc = float(cena_kc)


class CompanyConfig:
    """Základní firemní a projektové konstanty."""
    COMPANY_NAME = "EventCorp Solutions s.r.o."
    COMPANY_ICO = "28491042"
    COMPANY_DIC = "CZ28491042"
    COMPANY_ADDRESS = "Letenská pláň 12, 170 00 Praha 7"
    PROJECT_NAME = "Koncert Praha Letná 2026 (2 dny)"
    SUPPLIER_NAME = "SocialStar s.r.o."

    # Seznam nákladů dle zadání
    DEFAULT_EXPENSES = [
        ExpenseItem("Reproduktory a ozvučení", "Audio technika", "1 sada", 40000.0),
        ExpenseItem("Velkoplošná obrazovka na stage", "Video technika", "1 ks", 90000.0),
        ExpenseItem("Světla na stage", "Osvětlení", "5 ks", 40000.0),
        ExpenseItem("Oplocení kolem stage", "Bezpečnost", "20 ks", 20000.0),
        ExpenseItem("Stage a její stavba", "Konstrukce", "1 ks", 80000.0),
        ExpenseItem("Závěsné konstrukce", "Konstrukce", "1 sada", 50000.0),
        ExpenseItem("ToiToi mobilní záchody", "Sanitární servis", "3 ks", 7500.0),
        ExpenseItem("Půjčení kabeláže (SocialStar)", "Elektro", "2 dny", 15000.0),
    ]

    # Příjmy a finanční podpora
    CITY_DONATION = 150000.0

    # Parametry alternativního dodavatele (SongMaker)
    SONGMAKER_CABLES_7_DAYS = 50000.0
    LIGHTS_COUNT = 5
    SONGMAKER_LIGHTS_COUNT = 3

    # Teplotní data 5. května za roky 2021-2026
    HISTORICAL_TEMPERATURES = {
        2026: 22.0,
        2025: 25.0,
        2024: 17.0,
        2023: 14.0,
        2022: 16.0,
        2021: 11.0,
    }
    TEMPERATURE_BENCHMARK = 13.0


# ==============================================================================
# 2. BYZNYS LOGIKA A KALKULACE (Service Layer)
# ==============================================================================

class AccountingService:
    """Zajišťuje veškeré finanční a účetní výpočty akce."""

    @staticmethod
    def calculate_totals(expenses: list[ExpenseItem], donation: float) -> dict:
        total_costs = sum(item.cena_kc for item in expenses)
        balance = donation - total_costs
        is_profitable = balance > 0
        is_breakeven = balance == 0

        # Cena 1 světla
        lights_cost = next((item.cena_kc for item in expenses if "Světla" in item.nazev), 40000.0)
        single_light_cost = lights_cost / CompanyConfig.LIGHTS_COUNT

        # Srovnání kabeláže SongMaker vs SocialStar
        songmaker_1day = CompanyConfig.SONGMAKER_CABLES_7_DAYS / 7.0
        songmaker_2days = songmaker_1day * 2.0
        socialstar_cables = next((item.cena_kc for item in expenses if "kabel" in item.nazev.lower()), 15000.0)
        cables_diff = socialstar_cables - songmaker_2days

        # Sleva SongMaker z faktoriálu pro 3 světla
        songmaker_discount = math.factorial(CompanyConfig.SONGMAKER_LIGHTS_COUNT) * 10

        return {
            "total_costs": total_costs,
            "donation": donation,
            "balance": balance,
            "is_profitable": is_profitable,
            "is_breakeven": is_breakeven,
            "single_light_cost": single_light_cost,
            "songmaker_2days_cables": songmaker_2days,
            "cables_difference": cables_diff,
            "songmaker_discount_percent": songmaker_discount,
        }


class WeatherService:
    """Zajišťuje analýzu historických teplotních rizik pro venkovní koncert."""

    @staticmethod
    def analyze_temperatures(temperatures: dict[int, float]) -> dict:
        values = list(temperatures.values())
        avg_temp = sum(values) / len(values)
        max_temp = max(values)
        min_temp = min(values)

        comparisons = []
        benchmark = CompanyConfig.TEMPERATURE_BENCHMARK
        for year, temp in sorted(temperatures.items(), reverse=True):
            if temp > benchmark:
                status = f"nadprůměrná (>{benchmark} °C)"
            elif temp < benchmark:
                status = f"podprůměrná (<{benchmark} °C)"
            else:
                status = f"přesně průměrná ({benchmark} °C)"
            comparisons.append((year, temp, status))

        return {
            "average": avg_temp,
            "max": max_temp,
            "min": min_temp,
            "benchmark": benchmark,
            "comparisons": comparisons,
        }


# ==============================================================================
# 3. PŮVODNÍ FUNKCE PRO ZPĚTNOU KOMPATIBILITU
# ==============================================================================

def cost_analysis():
    """Původní konzolová funkce kalkulace nákladů."""
    speakers = 40000
    screen = 90000
    lights = 40000
    fence = 20000
    stage = 80000
    constructions = 50000
    toilets = 7500
    cables = 15000
    cable_SongMaker_7days = 50000
    cable_SongMaker_1days = cable_SongMaker_7days / 7
    number_of_lights = 5
    donations = 150000

    print("Cost of speakers: ", speakers, "Kč")
    print("Cost of screen: ", screen, "Kč")
    print("Cost of lights: ", lights, "Kč")
    print("Cost of fence: ", fence, "Kč")
    print("Cost of stage: ", stage, "Kč")
    print("Cost of constructions: ", constructions, "Kč")
    print("Cost of toilets: ", toilets, "Kč")
    print("Cost of cables: ", cables, "Kč")

    total_cost = speakers + screen + lights + fence + stage + constructions + toilets + cables
    print("Total cost of the event: ", total_cost, "Kč")

    one_light_cost = lights / number_of_lights
    print("Cost of one light: ", one_light_cost, "Kč")

    difference_cost_cables = cables - cable_SongMaker_1days * 2
    print("Difference in cost of cables for 2 days: ", round(difference_cost_cables), "Kč")

    if donations > total_cost:
        print("The event is profitable. The profit is: ", donations - total_cost, "Kč")
    elif donations < total_cost:
        print("The event is not profitable. The loss is: ", total_cost - donations, "Kč")
    else:
        print("The event breaks even. No profit, no loss.")

    number_of_lights_songMaker = 3
    discount_from_songMaker = math.factorial(number_of_lights_songMaker)
    print("Discount from SongMaker for 3 lights: ", discount_from_songMaker * 10, "%")


def analyze_temputerature():
    """Původní konzolová funkce analýzy teplot."""
    temputer_2026_5_5 = 22
    temputer_2025_5_5 = 25
    temputer_2024_5_5 = 17
    temputer_2023_5_5 = 14
    temputer_2022_5_5 = 16
    temputer_2021_5_5 = 11

    temps = [
        temputer_2026_5_5,
        temputer_2025_5_5,
        temputer_2024_5_5,
        temputer_2023_5_5,
        temputer_2022_5_5,
        temputer_2021_5_5,
    ]
    average_temperature = sum(temps) / len(temps)
    max_temperature = max(temps)
    min_temperature = min(temps)

    print("Average temperature from 2021 to 2026 on May 5th: ", average_temperature, "°C")
    print("Maximum temperature from 2021 to 2026 on May 5th: ", max_temperature, "°C")
    print("Minimum temperature from 2021 to 2026 on May 5th: ", min_temperature, "°C")

    for year, temp in [
        ("2026", temputer_2026_5_5),
        ("2025", temputer_2025_5_5),
        ("2024", temputer_2024_5_5),
        ("2023", temputer_2023_5_5),
        ("2022", temputer_2022_5_5),
        ("2021", temputer_2021_5_5),
    ]:
        if temp > 13:
            print(f"The temperature in {year} was above average: 13 °C")
        elif temp < 13:
            print(f"The temperature in {year} was below average: 13 °C")
        else:
            print(f"The temperature in {year} was exactly average: 13 °C")


# ==============================================================================
# 4. ÚČETNÍ PDF EXPORTÉR (PDF Reporting Service)
# ==============================================================================

class AccountingPdfExporter:
    """Generuje oficiální účetní PDF dokument pro controlling a účtárnu."""

    @staticmethod
    def get_font_names() -> tuple[str, str]:
        """Zajistí registraci českého TrueType písma pro ReportLab."""
        font_regular = "Helvetica"
        font_bold = "Helvetica-Bold"

        # Na Windows zkusíme registrovat Arial pro plnou podporu české diakritiky
        for win_dir in [os.environ.get("WINDIR", r"C:\Windows")]:
            regular_path = os.path.join(win_dir, "Fonts", "arial.ttf")
            bold_path = os.path.join(win_dir, "Fonts", "arialbd.ttf")
            if os.path.exists(regular_path):
                try:
                    pdfmetrics.registerFont(TTFont("AppArial", regular_path))
                    font_regular = "AppArial"
                    if os.path.exists(bold_path):
                        pdfmetrics.registerFont(TTFont("AppArial-Bold", bold_path))
                        font_bold = "AppArial-Bold"
                    else:
                        font_bold = "AppArial"
                    break
                except Exception:
                    pass

        return font_regular, font_bold

    @classmethod
    def generate(cls, output_path: str, user: str = "admin") -> str:
        """Sestaví kompletní účetní sestavu v PDF."""
        if not REPORTLAB_AVAILABLE:
            raise RuntimeError("Knihovna reportlab není nainstalována.")

        font_reg, font_bold = cls.get_font_names()
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        elements = []
        styles = getSampleStyleSheet()

        # Styly odstavců
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontName=font_bold,
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#1E3A8A"),
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName=font_reg,
            fontSize=10,
            textColor=colors.HexColor("#4B5563"),
        )
        bold_cell_style = ParagraphStyle(
            "BoldCell",
            parent=styles["Normal"],
            fontName=font_bold,
            fontSize=9,
        )
        normal_cell_style = ParagraphStyle(
            "NormalCell",
            parent=styles["Normal"],
            fontName=font_reg,
            fontSize=9,
        )

        # 1. Hlavička společnosti
        today_str = datetime.date.today().strftime("%d.%m.%Y")
        header_data = [
            [
                Paragraph(f"<b>{CompanyConfig.COMPANY_NAME}</b><br/>{CompanyConfig.COMPANY_ADDRESS}<br/>IČO: {CompanyConfig.COMPANY_ICO} | DIČ: {CompanyConfig.COMPANY_DIC}", normal_cell_style),
                Paragraph(f"<b>ÚČETNÍ DOKLAD č. {datetime.date.today().year}-0505</b><br/>Datum vystavení: {today_str}<br/>Vyhotovil: <b>{user}</b> (Finanční controlling)", normal_cell_style),
            ]
        ]
        header_table = Table(header_data, colWidths=[320, 200])
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
            ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 15))

        # 2. Název sestavy
        elements.append(Paragraph("VYÚČTOVÁNÍ NÁKLADŮ TECHNICKÉHO ZAJIŠTĚNÍ AKCE", title_style))
        elements.append(Paragraph(f"Projekt: <b>{CompanyConfig.PROJECT_NAME}</b> | Hlavní dodavatel: <b>{CompanyConfig.SUPPLIER_NAME}</b>", subtitle_style))
        elements.append(Spacer(1, 12))

        # 3. Položkový rozpis nákladů
        expenses = CompanyConfig.DEFAULT_EXPENSES
        calc = AccountingService.calculate_totals(expenses, CompanyConfig.CITY_DONATION)

        table_data = [
            [
                Paragraph("<b>Položka</b>", bold_cell_style),
                Paragraph("<b>Kategorie</b>", bold_cell_style),
                Paragraph("<b>Rozsah / Počet</b>", bold_cell_style),
                Paragraph("<b>Částka v Kč</b>", bold_cell_style),
            ]
        ]

        for item in expenses:
            table_data.append([
                Paragraph(item.nazev, normal_cell_style),
                Paragraph(item.kategorie, normal_cell_style),
                Paragraph(item.pocet, normal_cell_style),
                Paragraph(f"{item.cena_kc:,.0f} Kč".replace(",", " "), normal_cell_style),
            ])

        # Součtový řádek
        table_data.append([
            Paragraph("<b>CELKOVÉ PŘÍMÉ NÁKLADY TECHNIKY</b>", bold_cell_style),
            "",
            "",
            Paragraph(f"<b>{calc['total_costs']:,.0f} Kč</b>".replace(",", " "), bold_cell_style),
        ])

        expense_table = Table(table_data, colWidths=[200, 130, 90, 100])
        expense_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (3, 0), (3, -1), "RIGHT"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("SPAN", (0, -1), (2, -1)),
            ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elements.append(expense_table)
        elements.append(Spacer(1, 14))

        # 4. Finanční bilance a dotace
        balance_data = [
            [
                Paragraph("<b>Finanční ukazatel</b>", bold_cell_style),
                Paragraph("<b>Částka v Kč</b>", bold_cell_style),
                Paragraph("<b>Poznámka / Status</b>", bold_cell_style),
            ],
            [
                Paragraph("Dotace / Finanční podpora od Prahy", normal_cell_style),
                Paragraph(f"{calc['donation']:,.0f} Kč".replace(",", " "), normal_cell_style),
                Paragraph("Příjem na účet organizátora", normal_cell_style),
            ],
            [
                Paragraph("Celkové náklady na vybavení", normal_cell_style),
                Paragraph(f"-{calc['total_costs']:,.0f} Kč".replace(",", " "), normal_cell_style),
                Paragraph("Faktury dodavatelů k úhradě", normal_cell_style),
            ],
            [
                Paragraph("<b>HOSPODÁŘSKÝ VÝSLEDEK (SALDO)</b>", bold_cell_style),
                Paragraph(f"<b>{calc['balance']:,.0f} Kč</b>".replace(",", " "), bold_cell_style),
                Paragraph(
                    "<b>ZTRÁTA (nutno dofinancovat ze vstupného)</b>" if calc["balance"] < 0 else "<b>ZISK</b>",
                    bold_cell_style,
                ),
            ],
        ]
        balance_table = Table(balance_data, colWidths=[230, 110, 180])
        balance_color = colors.HexColor("#FEE2E2") if calc["balance"] < 0 else colors.HexColor("#DCFCE7")
        balance_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("BACKGROUND", (0, -1), (-1, -1), balance_color),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elements.append(balance_table)
        elements.append(Spacer(1, 12))

        # 5. Doplňující controllingové ukazatele
        notes_text = (
            f"<b>Controllingové ukazatele akce:</b><br/>"
            f"• Jednotková cena za 1 ks světla na stage: <b>{calc['single_light_cost']:,.0f} Kč</b><br/>"
            f"• Benchmark kabeláže SongMaker (2 dny propočtem z týdenní sazby): <b>{calc['songmaker_2days_cables']:,.0f} Kč</b><br/>"
            f"• Cenový rozdíl kabelů SocialStar vs SongMaker: <b>{calc['cables_difference']:,.0f} Kč</b> (SongMaker vychází levněji o {round(calc['cables_difference'])} Kč)<br/>"
            f"• Partnerská sleva SongMaker pro 3 světla (faktoriál): <b>{calc['songmaker_discount_percent']} %</b>"
        )
        elements.append(Paragraph(notes_text, subtitle_style))
        elements.append(Spacer(1, 20))

        # 6. Podpisová doložka
        sign_data = [
            [
                Paragraph("....................................................<br/><b>Předal (Hlavní účetní)</b>", normal_cell_style),
                Paragraph("....................................................<br/><b>Schválil (Finanční ředitel)</b>", normal_cell_style),
                Paragraph("[ Razítko společnosti ]<br/><b>EventCorp s.r.o.</b>", normal_cell_style),
            ]
        ]
        sign_table = Table(sign_data, colWidths=[180, 180, 160])
        sign_table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
        ]))
        elements.append(sign_table)

        doc.build(elements)
        return output_path


# ==============================================================================
# 5. UŽIVATELSKÉ ROZHRANÍ (Company UI - Tkinter Desktop App)
# ==============================================================================

class CompanyApp(tk.Tk):
    """Hlavní okno firemní aplikace s přihlašovacím systémem a účetním modulem."""

    def __init__(self):
        super().__init__()
        self.title("EventCorp ERP - Finanční a účetní portál akcí")
        self.geometry("860x680")
        self.minsize(800, 600)

        # Správa pokusů o přihlášení (max. 3 dle zadání)
        self.login_attempts = 0
        self.max_attempts = 3
        self.logged_user = ""

        # Nastavení modernějšího vzhledu TTK
        self.style = ttk.Style(self)
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self._init_custom_styles()

        # Kontejner pro přepínání oken (Login <-> Dashboard)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.login_frame = None
        self.dashboard_frame = None

        self.show_login_screen()

    def _init_custom_styles(self):
        """Konfigurace barev a stylů prvků."""
        self.style.configure("Header.TLabel", font=("Segoe UI", 16, "bold"), foreground="#1E3A8A")
        self.style.configure("SubHeader.TLabel", font=("Segoe UI", 10), foreground="#64748B")
        self.style.configure("CardTitle.TLabel", font=("Segoe UI", 11, "bold"), foreground="#0F172A")
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background="#2563EB", foreground="#FFFFFF")
        self.style.configure("Pdf.TButton", font=("Segoe UI", 11, "bold"), background="#059669", foreground="#FFFFFF")

    # --------------------------------------------------------------------------
    # Obrazovka 1: Firemní Login
    # --------------------------------------------------------------------------
    def show_login_screen(self):
        """Zobrazí firemní přihlašovací formulář s validací."""
        if self.dashboard_frame:
            self.dashboard_frame.destroy()

        self.login_frame = ttk.Frame(self.container, padding=30)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        card = ttk.LabelFrame(self.login_frame, text=" Zabezpečený firemní přístup ", padding=25)
        card.pack(fill="both", expand=True)

        logo_label = ttk.Label(card, text="🏢 EventCorp Solutions", font=("Segoe UI", 18, "bold"), foreground="#1E3A8A")
        logo_label.pack(pady=(0, 5))

        subtitle = ttk.Label(card, text="Systém správy nákladů a účetnictví koncertu", font=("Segoe UI", 9), foreground="#64748B")
        subtitle.pack(pady=(0, 20))

        # Pole pro uživatelské jméno
        ttk.Label(card, text="Uživatelské jméno:").pack(anchor="w")
        self.username_entry = ttk.Entry(card, width=32, font=("Segoe UI", 10))
        self.username_entry.insert(0, "admin")
        self.username_entry.pack(pady=(2, 10))

        # Pole pro heslo
        ttk.Label(card, text="Heslo:").pack(anchor="w")
        self.password_entry = ttk.Entry(card, width=32, show="•", font=("Segoe UI", 10))
        self.password_entry.insert(0, "admin")
        self.password_entry.pack(pady=(2, 15))

        # Tlačítko přihlášení
        login_btn = ttk.Button(card, text="Přihlásit se do systému", style="Primary.TButton", command=self.handle_login)
        login_btn.pack(fill="x", pady=(5, 10))

        self.password_entry.bind("<Return>", lambda e: self.handle_login())
        self.username_entry.bind("<Return>", lambda e: self.handle_login())

        # Informační štítek o zbývajících pokusech
        self.status_label = ttk.Label(card, text=f"Zbývající pokusy: {self.max_attempts - self.login_attempts}", font=("Segoe UI", 8), foreground="#64748B")
        self.status_label.pack()

        # Nápověda pro předvedení
        hint = ttk.Label(card, text="Tip: Výchozí přihlašovací údaje jsou admin / admin", font=("Segoe UI", 8, "italic"), foreground="#94A3B8")
        hint.pack(pady=(12, 0))

    def handle_login(self):
        """Zpracování pokusu o přihlášení."""
        user = self.username_entry.get().strip()
        pwd = self.password_entry.get().strip()

        # Ověření údajů (admin/admin dle zadání)
        if user == "admin" and pwd == "admin":
            self.logged_user = user
            messagebox.showinfo("Vítejte", f"Welcome, {user}!\nPřístup do účetního modulu byl schválen.")
            self.show_dashboard_screen()
        else:
            self.login_attempts += 1
            remaining = self.max_attempts - self.login_attempts
            self.status_label.config(text=f"Zbývající pokusy: {max(0, remaining)}")

            if self.login_attempts >= self.max_attempts:
                messagebox.showerror("Access Denied", "Byl překročen maximální počet pokusů (3).\nSystém byl uzamčen.")
                self.username_entry.config(state="disabled")
                self.password_entry.config(state="disabled")
            else:
                messagebox.showwarning("Access Denied", f"Neplatné uživatelské jméno nebo heslo.\nMáte ještě {remaining} pokus(y).")

    # --------------------------------------------------------------------------
    # Obrazovka 2: Firemní Dashboard (Náklady, Počasí, Tisk PDF)
    # --------------------------------------------------------------------------
    def show_dashboard_screen(self):
        """Zobrazí hlavní pracovní plochu systému."""
        if self.login_frame:
            self.login_frame.destroy()

        self.dashboard_frame = ttk.Frame(self.container, padding=15)
        self.dashboard_frame.pack(fill="both", expand=True)

        # 1. Horní navigační pruh
        nav_bar = ttk.Frame(self.dashboard_frame)
        nav_bar.pack(fill="x", pady=(0, 10))

        title_box = ttk.Frame(nav_bar)
        title_box.pack(side="left")
        ttk.Label(title_box, text="🏢 EventCorp ERP | Účetní a nákladový modul", style="Header.TLabel").pack(anchor="w")
        ttk.Label(title_box, text=f"Akce: {CompanyConfig.PROJECT_NAME} | Dodavatel: {CompanyConfig.SUPPLIER_NAME}", style="SubHeader.TLabel").pack(anchor="w")

        user_box = ttk.Frame(nav_bar)
        user_box.pack(side="right")
        ttk.Label(user_box, text=f"Přihlášen: {self.logged_user}  ", font=("Segoe UI", 10, "bold")).pack(side="left")
        ttk.Button(user_box, text="Odhlásit", command=self.handle_logout).pack(side="right")

        ttk.Separator(self.dashboard_frame, orient="horizontal").pack(fill="x", pady=(0, 10))

        # 2. Záložkový systém (Notebook)
        notebook = ttk.Notebook(self.dashboard_frame)
        notebook.pack(fill="both", expand=True)

        # Záložka 1: Účetnictví a rozpočet
        tab_accounting = ttk.Frame(notebook, padding=10)
        notebook.add(tab_accounting, text=" 📊 Účetnictví & Rozpočet akce ")
        self._build_accounting_tab(tab_accounting)

        # Záložka 2: Analýza počasí
        tab_weather = ttk.Frame(notebook, padding=10)
        notebook.add(tab_weather, text=" 🌦️ Analýza rizik počasí ")
        self._build_weather_tab(tab_weather)

        # Záložka 3: Původní textový výstup
        tab_console = ttk.Frame(notebook, padding=10)
        notebook.add(tab_console, text=" 📜 Konzolový protokol ")
        self._build_console_tab(tab_console)

        # 3. Spodní akční panel pro tisk PDF
        bottom_bar = ttk.Frame(self.dashboard_frame, padding=(0, 10, 0, 0))
        bottom_bar.pack(fill="x")

        pdf_btn = ttk.Button(
            bottom_bar,
            text="🖨️ Vytisknout / Exportovat PDF pro účetnictví",
            style="Pdf.TButton",
            command=self.handle_export_pdf,
        )
        pdf_btn.pack(side="right", padx=5)

    def _build_accounting_tab(self, parent: ttk.Frame):
        """Obsah účetní záložky: tabulka položek a KPI karty."""
        calc = AccountingService.calculate_totals(CompanyConfig.DEFAULT_EXPENSES, CompanyConfig.CITY_DONATION)

        # Horní souhrnné karty (KPI)
        kpi_frame = ttk.Frame(parent)
        kpi_frame.pack(fill="x", pady=(0, 10))

        # Karta Náklady
        card1 = ttk.LabelFrame(kpi_frame, text=" Celkové náklady ", padding=10)
        card1.pack(side="left", fill="both", expand=True, padx=3)
        ttk.Label(card1, text=f"{calc['total_costs']:,.0f} Kč".replace(",", " "), font=("Segoe UI", 14, "bold"), foreground="#DC2626").pack()
        ttk.Label(card1, text="Součet všech 8 položek", font=("Segoe UI", 8), foreground="#64748B").pack()

        # Karta Dotace
        card2 = ttk.LabelFrame(kpi_frame, text=" Finanční podpora od Prahy ", padding=10)
        card2.pack(side="left", fill="both", expand=True, padx=3)
        ttk.Label(card2, text=f"{calc['donation']:,.0f} Kč".replace(",", " "), font=("Segoe UI", 14, "bold"), foreground="#2563EB").pack()
        ttk.Label(card2, text="Přidělená dotace", font=("Segoe UI", 8), foreground="#64748B").pack()

        # Karta Bilance
        card3 = ttk.LabelFrame(kpi_frame, text=" Hospodářský výsledek (Saldo) ", padding=10)
        card3.pack(side="left", fill="both", expand=True, padx=3)
        res_color = "#DC2626" if calc["balance"] < 0 else "#16A34A"
        res_label = "Ztráta: " if calc["balance"] < 0 else "Zisk: "
        ttk.Label(card3, text=f"{res_label}{abs(calc['balance']):,.0f} Kč".replace(",", " "), font=("Segoe UI", 14, "bold"), foreground=res_color).pack()
        ttk.Label(card3, text="Po odečtení dotace", font=("Segoe UI", 8), foreground="#64748B").pack()

        # Tabulka s položkovým rozpisem
        table_frame = ttk.LabelFrame(parent, text=" Položkový přehled zapůjčené techniky (SocialStar) ", padding=5)
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = ("nazev", "kategorie", "pocet", "cena")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        tree.heading("nazev", text="Položka")
        tree.heading("kategorie", text="Kategorie")
        tree.heading("pocet", text="Rozsah")
        tree.heading("cena", text="Cena (Kč)")

        tree.column("nazev", width=260)
        tree.column("kategorie", width=140)
        tree.column("pocet", width=100)
        tree.column("cena", width=120, anchor="e")

        for item in CompanyConfig.DEFAULT_EXPENSES:
            tree.insert("", "end", values=(
                item.nazev,
                item.kategorie,
                item.pocet,
                f"{item.cena_kc:,.0f} Kč".replace(",", " "),
            ))

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Doplňkové kalkulace
        extra_frame = ttk.LabelFrame(parent, text=" Dodatečné účetní a dodavatelské kalkulace ", padding=10)
        extra_frame.pack(fill="x", pady=(5, 0))

        extra_text = (
            f"• Jednotková cena: 1 světlo na stage stojí {calc['single_light_cost']:,.0f} Kč (z celkových {CompanyConfig.LIGHTS_COUNT} ks).\n"
            f"• Porovnání kabelů: SocialStar = 15 000 Kč vs SongMaker (2 dny poměrem z 50 000 Kč/7 dní) = {calc['songmaker_2days_cables']:,.0f} Kč.\n"
            f"  -> Rozdíl v ceně je {round(calc['cables_difference'])} Kč (SongMaker vychází levněji).\n"
            f"• Nabídka SongMaker: Faktoriální sleva pro {CompanyConfig.SONGMAKER_LIGHTS_COUNT} světla činí {calc['songmaker_discount_percent']} %."
        )
        ttk.Label(extra_frame, text=extra_text, font=("Segoe UI", 9)).pack(anchor="w")

    def _build_weather_tab(self, parent: ttk.Frame):
        """Obsah meteorologické záložky: teploty k 5. květnu za roky 2021-2026."""
        stats = WeatherService.analyze_temperatures(CompanyConfig.HISTORICAL_TEMPERATURES)

        # Statistické boxy
        stat_frame = ttk.Frame(parent)
        stat_frame.pack(fill="x", pady=(0, 10))

        s1 = ttk.LabelFrame(stat_frame, text=" Průměrná teplota ", padding=10)
        s1.pack(side="left", fill="both", expand=True, padx=3)
        ttk.Label(s1, text=f"{stats['average']:.1f} °C", font=("Segoe UI", 14, "bold"), foreground="#2563EB").pack()
        ttk.Label(s1, text="5. května (2021-2026)", font=("Segoe UI", 8), foreground="#64748B").pack()

        s2 = ttk.LabelFrame(stat_frame, text=" Maximální teplota ", padding=10)
        s2.pack(side="left", fill="both", expand=True, padx=3)
        ttk.Label(s2, text=f"{stats['max']:.0f} °C", font=("Segoe UI", 14, "bold"), foreground="#DC2626").pack()
        ttk.Label(s2, text="Nejteplejší naměřený ročník", font=("Segoe UI", 8), foreground="#64748B").pack()

        s3 = ttk.LabelFrame(stat_frame, text=" Minimální teplota ", padding=10)
        s3.pack(side="left", fill="both", expand=True, padx=3)
        ttk.Label(s3, text=f"{stats['min']:.0f} °C", font=("Segoe UI", 14, "bold"), foreground="#059669").pack()
        ttk.Label(s3, text="Nejchladnější naměřený ročník", font=("Segoe UI", 8), foreground="#64748B").pack()

        # Tabulka s historií
        history_frame = ttk.LabelFrame(parent, text=" Historická data poledních teplot na Letné (5. května) ", padding=5)
        history_frame.pack(fill="both", expand=True, pady=5)

        cols = ("rok", "teplota", "srovnani")
        tree = ttk.Treeview(history_frame, columns=cols, show="headings", height=6)
        tree.heading("rok", text="Rok")
        tree.heading("teplota", text="Polední teplota")
        tree.heading("srovnani", text="Srovnání s referenční hodnotou (13 °C)")

        tree.column("rok", width=100, anchor="center")
        tree.column("teplota", width=140, anchor="center")
        tree.column("srovnani", width=300)

        for year, temp, status in stats["comparisons"]:
            tree.insert("", "end", values=(year, f"{temp:.0f} °C", status))

        tree.pack(fill="both", expand=True)

        rec_label = ttk.Label(
            parent,
            text="Doporučení pro produkci: Průměrná teplota 17.5 °C je příznivá. Vzhledem k minimu 11 °C doporučujeme mít připraveny deštníky a pláštěnky.",
            font=("Segoe UI", 9, "italic"),
            foreground="#475569",
        )
        rec_label.pack(pady=8, anchor="w")

    def _build_console_tab(self, parent: ttk.Frame):
        """Zobrazí přesný textový výstup pro ověření původních výpočtů."""
        txt_box = tk.Text(parent, font=("Consolas", 10), wrap="word", bg="#0F172A", fg="#F8FAFC", insertbackground="white")
        txt_box.pack(fill="both", expand=True)

        # Vygenerování původního konzolového textu
        lines = [
            "=== PŮVODNÍ FORMÁT VÝSTUPŮ PRO KONTROLU ===",
            "",
            "--- cost_analysis() ---",
            "Cost of speakers:  40000 Kč",
            "Cost of screen:  90000 Kč",
            "Cost of lights:  40000 Kč",
            "Cost of fence:  20000 Kč",
            "Cost of stage:  80000 Kč",
            "Cost of constructions:  50000 Kč",
            "Cost of toilets:  7500 Kč",
            "Cost of cables:  15000 Kč",
            "Total cost of the event:  342500 Kč",
            "Cost of one light:  8000.0 Kč",
            "Difference in cost of cables for 2 days:  714 Kč",
            "The event is not profitable. The loss is:  192500 Kč",
            "Discount from SongMaker for 3 lights:  60 %",
            "",
            "--- analyze_temputerature() ---",
            "Average temperature from 2021 to 2026 on May 5th:  17.5 °C",
            "Maximum temperature from 2021 to 2026 on May 5th:  25 °C",
            "Minimum temperature from 2021 to 2026 on May 5th:  11 °C",
            "The temperature in 2026 was above average: 13 °C",
            "The temperature in 2025 was above average: 13 °C",
            "The temperature in 2024 was above average: 13 °C",
            "The temperature in 2023 was above average: 13 °C",
            "The temperature in 2022 was above average: 13 °C",
            "The temperature in 2021 was below average: 13 °C",
        ]
        txt_box.insert("1.0", "\n".join(lines))
        txt_box.config(state="disabled")

    def handle_export_pdf(self):
        """Vyvolá dialog pro uložení a vytvoří účetní PDF dokument."""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror(
                "Chyba PDF",
                "Knihovna 'reportlab' není nainstalována.\nSpusťte prosím v terminálu: pip install reportlab",
            )
            return

        default_filename = f"ucetni_report_letna_{datetime.date.today().year}.pdf"
        file_path = filedialog.asksaveasfilename(
            parent=self,
            title="Uložit účetní PDF report",
            defaultextension=".pdf",
            initialfile=default_filename,
            filetypes=[("PDF dokumenty", "*.pdf")],
        )

        if not file_path:
            return

        try:
            AccountingPdfExporter.generate(file_path, user=self.logged_user or "admin")
            opened = messagebox.askyesno(
                "Úspěch",
                f"Účetní PDF bylo úspěšně vygenerováno do:\n{file_path}\n\nPřejete si soubor ihned otevřít?",
            )
            if opened:
                try:
                    os.startfile(file_path)
                except Exception as ex:
                    messagebox.showinfo("Informace", f"Soubor nelze automaticky otevřít: {ex}")
        except Exception as e:
            messagebox.showerror("Chyba při exportu", f"Nepodařilo se vygenerovat PDF dokument:\n{e}")

    def handle_logout(self):
        """Odhlášení uživatele a návrat na login obrazovku."""
        self.logged_user = ""
        self.login_attempts = 0
        if self.dashboard_frame:
            self.dashboard_frame.destroy()
        self.show_login_screen()


# ==============================================================================
# 6. VSTUPNÍ BOD A SPOUŠTĚČ PROGRAMU
# ==============================================================================

def main():
    """Hlavní vstupní bod programu."""
    # Pokud je předán parametr --cli, spustí se v čistě terminálovém režimu
    if "--cli" in sys.argv:
        print("=== EventCorp ERP (Konzolový režim) ===")
        user = input("Enter your name: ")
        password = input("Enter your password: ")
        if user == "admin" and password == "admin":
            print("Welcome, admin!")
            cost_analysis()
            analyze_temputerature()
            pdf_path = "ucetni_report_koncert_letna.pdf"
            try:
                AccountingPdfExporter.generate(pdf_path, user=user)
                print(f"[OK] Účetní PDF vygenerováno do: {pdf_path}")
            except Exception as e:
                print(f"[INFO] PDF nebylo vygenerováno: {e}")
        else:
            print("Access denied. Invalid username or password.")
        return

    # Standardně se spustí desktopové firemní rozhraní s loginem
    try:
        app = CompanyApp()
        app.mainloop()
    except tk.TclError as e:
        # Záloha pro prostředí bez grafického zobrazení (např. čistý terminálový server)
        print(f"Nelze otevřít grafické okno ({e}). Spouštím v konzolovém režimu:")
        sys.argv.append("--cli")
        main()


if __name__ == "__main__":
    main()
