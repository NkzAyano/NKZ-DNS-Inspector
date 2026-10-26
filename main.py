
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from datetime import datetime

try:
    import dns.resolver
    import dns.exception
    DNS_AVAILABLE = True
except ImportError:
    DNS_AVAILABLE = False


BG = "#090B14"
PANEL = "#111629"
INPUT = "#1A223A"
PURPLE = "#A855F7"
BLUE = "#38BDF8"
WHITE = "#E8ECF8"
MUTED = "#9AA6C4"
GREEN = "#4ADE80"
RED = "#FB7185"

RECORD_TYPES = ["A", "AAAA", "MX", "TXT", "NS", "CNAME", "SOA"]


class NKZDNSInspector(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("NKZ DNS Inspector")
        self.geometry("900x620")
        self.minsize(720, 500)
        self.configure(bg=BG)

        self.results = []
        self._configure_style()
        self._create_interface()

    def _configure_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=30,
            borderwidth=0,
            font=("Consolas", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=INPUT,
            foreground=BLUE,
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )

        style.map(
            "Treeview",
            background=[("selected", "#382054")],
            foreground=[("selected", WHITE)]
        )

    def _create_interface(self):
        header = tk.Frame(self, bg=BG)
        header.pack(fill="x", padx=24, pady=(20, 5))

        tk.Label(
            header,
            text="NKZ",
            font=("Segoe UI", 28, "bold"),
            bg=BG,
            fg=PURPLE
        ).pack(side="left")

        tk.Label(
            header,
            text=" DNS INSPECTOR",
            font=("Segoe UI", 21, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(side="left")

        tk.Label(
            self,
            text="DNS LOOKUP  /  NETWORK INTELLIGENCE",
            font=("Consolas", 9),
            bg=BG,
            fg=BLUE
        ).pack(anchor="w", padx=28, pady=(0, 18))

        search = tk.Frame(
            self,
            bg=PANEL,
            highlightbackground="#29324E",
            highlightthickness=1
        )
        search.pack(fill="x", padx=24, pady=(0, 16))

        tk.Label(
            search,
            text="DOMÍNIO",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 5))

        self.domain_entry = tk.Entry(
            search,
            bg=INPUT,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Consolas", 12)
        )
        self.domain_entry.insert(0, "example.com")
        self.domain_entry.grid(
            row=1, column=0, sticky="ew",
            padx=14, pady=(0, 14), ipady=9
        )

        tk.Label(
            search,
            text="REGISTRO",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).grid(row=0, column=1, sticky="w", padx=8, pady=(12, 5))

        self.record_var = tk.StringVar(value="ALL")

        self.record_combo = ttk.Combobox(
            search,
            textvariable=self.record_var,
            values=["ALL"] + RECORD_TYPES,
            state="readonly",
            width=10
        )
        self.record_combo.grid(
            row=1, column=1, padx=8, pady=(0, 14), ipady=7
        )

        self.lookup_btn = tk.Button(
            search,
            text="CONSULTAR",
            command=self.start_lookup,
            bg=PURPLE,
            fg="white",
            activebackground="#9333EA",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=10
        )
        self.lookup_btn.grid(
            row=1, column=2, padx=(8, 14), pady=(0, 14)
        )

        search.columnconfigure(0, weight=1)

        status_frame = tk.Frame(self, bg=BG)
        status_frame.pack(fill="x", padx=26, pady=(0, 8))

        self.status = tk.Label(
            status_frame,
            text="PRONTO • Digite um domínio.",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 9)
        )
        self.status.pack(side="left")

        self.counter = tk.Label(
            status_frame,
            text="0 RESULTADOS",
            bg=BG,
            fg=BLUE,
            font=("Consolas", 9, "bold")
        )
        self.counter.pack(side="right")

        table_frame = tk.Frame(
            self,
            bg=PANEL,
            highlightbackground="#29324E",
            highlightthickness=1
        )
        table_frame.pack(
            fill="both", expand=True,
            padx=24, pady=(0, 12)
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=("type", "value", "ttl"),
            show="headings"
        )

        self.table.heading("type", text="TIPO")
        self.table.heading("value", text="VALOR / DESTINO")
        self.table.heading("ttl", text="TTL (s)")

        self.table.column("type", width=90, anchor="center")
        self.table.column("value", width=550, anchor="w")
        self.table.column("ttl", width=90, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )

        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.pack(
            side="left", fill="both", expand=True,
            padx=(8, 0), pady=8
        )
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)

        footer = tk.Frame(self, bg=BG)
        footer.pack(fill="x", padx=24, pady=(0, 16))

        tk.Button(
            footer,
            text="EXPORTAR TXT",
            command=self.export_txt,
            bg=INPUT,
            fg=BLUE,
            activebackground="#25304D",
            activeforeground=WHITE,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=9
        ).pack(side="left")

        tk.Label(
            footer,
            text="NKZ CYBERSECURITY",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 9)
        ).pack(side="right")

        self.domain_entry.bind(
            "<Return>",
            lambda event: self.start_lookup()
        )

        if not DNS_AVAILABLE:
            self.status.config(
                text="Instale as dependências pelo requirements.txt.",
                fg=RED
            )

    @staticmethod
    def valid_domain(domain):
        if not domain or len(domain) > 253:
            return False

        if domain.endswith("."):
            domain = domain[:-1]

        labels = domain.split(".")

        if len(labels) < 2:
            return False

        for label in labels:
            if (
                not label
                or len(label) > 63
                or label.startswith("-")
                or label.endswith("-")
                or not all(c.isalnum() or c == "-" for c in label)
            ):
                return False

        return True

    def start_lookup(self):
        domain = self.domain_entry.get().strip().rstrip(".")

        if not self.valid_domain(domain):
            messagebox.showwarning(
                "Domínio inválido",
                "Digite um domínio válido, como example.com."
            )
            return

        if not DNS_AVAILABLE:
            messagebox.showerror(
                "Dependência ausente",
                "Execute: py -m pip install -r requirements.txt"
            )
            return

        self.lookup_btn.config(state="disabled", text="CONSULTANDO...")
        self.status.config(text=f"CONSULTANDO • {domain}", fg=BLUE)
        self.counter.config(text="AGUARDE...")

        for item in self.table.get_children():
            self.table.delete(item)

        self.results = []

        threading.Thread(
            target=self.lookup_worker,
            args=(domain, self.record_var.get()),
            daemon=True
        ).start()

    def lookup_worker(self, domain, selected_type):
        results = []
        record_types = (
            RECORD_TYPES if selected_type == "ALL"
            else [selected_type]
        )

        resolver = dns.resolver.Resolver()
        resolver.timeout = 3
        resolver.lifetime = 5

        for record_type in record_types:
            try:
                answer = resolver.resolve(
                    domain,
                    record_type,
                    raise_on_no_answer=False
                )

                if answer.rrset is None:
                    continue

                ttl = answer.rrset.ttl

                for record in answer:
                    results.append(
                        (record_type, record.to_text(), str(ttl))
                    )

            except (
                dns.resolver.NXDOMAIN,
                dns.resolver.NoAnswer,
                dns.resolver.NoNameservers,
                dns.exception.DNSException,
                OSError
            ):
                continue

            except Exception:
                continue

        self.after(
            0, self.finish_lookup, domain, results
        )

    def finish_lookup(self, domain, results):
        self.results = results

        for record_type, value, ttl in results:
            self.table.insert(
                "",
                "end",
                values=(record_type, value, ttl)
            )

        self.counter.config(
            text=f"{len(results)} RESULTADO(S)"
        )

        if results:
            self.status.config(
                text=f"CONCLUÍDO • {domain}",
                fg=GREEN
            )
        else:
            self.status.config(
                text="NENHUM REGISTRO ENCONTRADO",
                fg=RED
            )

        self.lookup_btn.config(
            state="normal",
            text="CONSULTAR"
        )

    def export_txt(self):
        if not self.results:
            messagebox.showinfo(
                "Sem resultados",
                "Realize uma consulta antes de exportar."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Exportar relatório DNS",
            defaultextension=".txt",
            initialfile="NKZ_DNS_Report.txt",
            filetypes=[("Arquivo de texto", "*.txt")]
        )

        if not path:
            return

        domain = self.domain_entry.get().strip()

        with open(path, "w", encoding="utf-8") as file:
            file.write("NKZ DNS INSPECTOR\n")
            file.write("=" * 50 + "\n")
            file.write(f"Domínio: {domain}\n")
            file.write(
                "Data: "
                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                + "\n\n"
            )

            for record_type, value, ttl in self.results:
                file.write(
                    f"[{record_type}] TTL={ttl} | {value}\n"
                )

        messagebox.showinfo(
            "Sucesso",
            f"Relatório exportado:\n{path}"
        )


if __name__ == "__main__":
    app = NKZDNSInspector()
    app.mainloop()
