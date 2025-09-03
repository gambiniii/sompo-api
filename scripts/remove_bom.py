from pathlib import Path

# encontra alembic.ini relativo à raiz do projeto (dois níveis acima do script)
p = Path(__file__).resolve().parents[1] / "alembic.ini"
text = p.read_text(encoding="utf-8-sig")   # lê removendo BOM se existir
p.write_text(text, encoding="utf-8")        # regrava sem BOM
print("rewrote", p)