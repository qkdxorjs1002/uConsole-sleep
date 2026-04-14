import os


def find_drm_panel():
    DRM_PATH = "/sys/class/drm"

    for panel in os.listdir(DRM_PATH):
        panel_path = os.path.join(DRM_PATH, panel)

        if "DSI" in panel:
            return panel_path

    return ""


if __name__ == "__main__":
    print(find_drm_panel())
