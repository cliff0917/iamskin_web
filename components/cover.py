import feffery_antd_components as fac

import globals

def serve():
    cover = fac.AntdImage(
        src=f"{globals.config['img_path']}/cover.png",
        preview=False,
    )
    return cover
