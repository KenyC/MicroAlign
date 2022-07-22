import sublime_plugin


class MicroAlignMultipleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        sel  = view.sel()

        if len(sel) == 1:
            return

        cols    = [view.rowcol(region.begin())[1] for region in sel]
        max_col = max(cols)

        for (region, ncols) in zip(sel, cols):
            length = max_col - ncols
            view.insert(edit, region.begin(), ' ' * length)

