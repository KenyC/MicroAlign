import sublime_plugin


class MicroAlignMultipleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        sel  = view.sel()

        if len(sel) == 1:
            return

        # Sometimes, multiple selections are not oriented the same way:
        #   .----|
        #   |---------.
        #     |---------.
        # This frequently happens when using Ctrl+D, and the first selection is backwards
        # In case selection regions don't all cursor in the same position, we use a majority rule to decide whether to align with left or right boundary of the region
        # With a preference for left boundary in case of ties (which is what one wants 67.8 % of the times)

        # True if in most regions, a is before b false otherwise
        majority_order = sum(
            1 if region.a <= region.b else -1
            for region in sel
        ) >= 0

        # Which position to align
        anchors = [
            region.a if majority_order == (region.a <= region.b)
            else region.b
            for region in sel
        ]

        cols = [
            view.rowcol(anchor)[1] 
            for anchor in anchors
        ]
        max_col = max(cols)

        for (anchor, ncols) in zip(anchors, cols):
            length = max_col - ncols
            view.insert(edit, anchor, ' ' * length)

