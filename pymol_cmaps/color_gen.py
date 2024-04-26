from __future__ import annotations
from pathlib import Path
from matplotlib import colors as mpl_colors
from matplotlib import colormaps as mpl_cmaps


class CmapProcessor:
    def __init__(self, 
                 cmap_iter: Iterable[tuple[str, mpl_colors.Colormap]],
                 ) -> CmapProcessor:
        self._iter = cmap_iter
        self.pymol_cmaps = {}

    def process(self):
        for name, cmap in self._iter:
            hex_list = [mpl_colors.rgb2hex(color).replace('#', '0x') \
                    for color in cmap(range(cmap.N))]
            self.pymol_cmaps[name] = ' '.join(hex_list)

    def save(self, out: str, short: str | None  = None) -> None:
        out = Path(out)
        if not short:
            short = out.stem

        breakpoint()
        with open(out, 'w') as output:
            for k, v in self.pymol_cmaps.items():
                output.write(f"{k} = '''{v}'''\n")
            breakpoint()
            import_str = f"\nif __name__ == 'pymol':\n    import {out.stem} as {short}"
            output.write(import_str)


def main():
    mpl_processor = CmapProcessor(
            cmap_iter = mpl_cmaps._cmaps.items()
            )
    mpl_processor.process()
    mpl_processor.save('mpl_pymol.py', 'cm')

    import cmasher as cmr
    cmr_processor = CmapProcessor(
            cmap_iter = ((name, cmr.__dict__[name]) for name in cmr.get_cmap_list())
            )
    cmr_processor.process()
    cmr_processor.save('cmasher_pymol.py', 'cmr')

if __name__ == '__main__':
    main()
