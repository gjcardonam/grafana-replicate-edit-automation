import json
import os
from deepdiff import DeepDiff

MODIFIED_PANEL_PATH = "panel/modified-panel.json"
REPL_DASH_PATH = "dashboards/replicate/dashboards/general"
DASHBOARD_UID = "dashboard-2af4fa37-a4c8-41f8-a045-5c010869b172"
DASHBOARD_FILENAME = f"{DASHBOARD_UID}.json"

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def sync_panel():
    panel = load_json(MODIFIED_PANEL_PATH)
    panel_id = panel.get("id")
    if not panel_id:
        print("❌ No se encontró ID de panel en el JSON.")
        return

    path = os.path.join(REPL_DASH_PATH, DASHBOARD_FILENAME)
    if not os.path.exists(path):
        print(f"❌ No se encontró el dashboard {DASHBOARD_FILENAME}")
        return

    dashboard = load_json(path)
    panels = dashboard["spec"].get("panels", [])

    for idx, p in enumerate(panels):
        if p["id"] == panel_id:
            print(f"✅ Panel {panel_id} encontrado. Reemplazando contenido (manteniendo posición)...")
            grid_pos = p.get("gridPos", {})
            # Reemplaza todo el panel por el nuevo, pero preserva la posición
            new_panel = panel.copy()
            new_panel["gridPos"] = grid_pos
            panels[idx] = new_panel
            dashboard["spec"]["panels"] = panels
            save_json(path, dashboard)
            print(f"💾 Guardado: {path}")
            return

    # Panel no encontrado: agregar al final
    print(f"➕ Panel {panel_id} no existe. Agregando al dashboard.")
    panels.append(panel)
    dashboard["spec"]["panels"] = panels
    save_json(path, dashboard)
    print(f"💾 Guardado: {path}")

if __name__ == "__main__":
    sync_panel()