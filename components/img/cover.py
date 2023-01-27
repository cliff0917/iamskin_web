import feffery_antd_components as fac

import globals

def serve():
    cover = fac.AntdImage(
        src=f"{globals.config['assets_path']}/common/img/cover.png",
        preview=False,
    )
    return cover