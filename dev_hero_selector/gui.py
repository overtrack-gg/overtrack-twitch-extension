from threading import Thread
from typing import Optional, List, Callable, Dict, Union

import wx

Player = Dict[str, Union[str, Optional[int]]]
Team = Dict[str, Dict[str, List[Player]]]
Callback = Callable[[Team], None]

heroes = ['dva', 'orisa', 'reinhardt', 'roadhog', 'winston', 'hammond', 'zarya', 'ashe',
          'bastion', 'doomfist', 'genji', 'hanzo', 'junkrat', 'mccree', 'mei', 'pharah',
          'reaper', 'soldier', 'sombra', 'symmetra', 'torbjorn', 'tracer', 'widowmaker',
          'ana', 'baptiste', 'brigitte', 'lucio', 'mercy', 'moira', 'zenyatta']


class PlayerPanel(wx.Panel):
    def __init__(self, parent: 'ScoreboardGui', data: Player) -> None:
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.data = data

        name = wx.TextCtrl(self, value=data['name'])
        dropdown = wx.ComboBox(self, value=data['current_hero'], choices=heroes, style=wx.CB_READONLY)
        kills_label = wx.StaticText(self, label="Kills")
        kills = wx.SpinCtrl(self)
        deaths_label = wx.StaticText(self, label="Deaths")
        deaths = wx.SpinCtrl(self)
        res_label = wx.StaticText(self, label="Resurrects")
        res = wx.SpinCtrl(self)
        res.Disable()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(name, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(dropdown, 0, wx.EXPAND | wx.ALL, 5)

        grid_sizer = wx.FlexGridSizer(3, 2, 0, 0)
        grid_sizer.Add(kills_label, 0, wx.EXPAND | wx.ALL, 5)
        grid_sizer.Add(kills, 0, wx.EXPAND | wx.ALL, 5)
        grid_sizer.Add(deaths_label, 0, wx.EXPAND | wx.ALL, 5)
        grid_sizer.Add(deaths, 0, wx.EXPAND | wx.ALL, 5)
        grid_sizer.Add(res_label, 0, wx.EXPAND | wx.ALL, 5)
        grid_sizer.Add(res, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(grid_sizer)

        self.SetSizerAndFit(sizer)
        self.res = res

        name.Bind(wx.EVT_TEXT, self.set_name)
        dropdown.Bind(wx.EVT_COMBOBOX, self.set_hero)
        kills.Bind(wx.EVT_SPINCTRL, self.set_kills)
        deaths.Bind(wx.EVT_SPINCTRL, self.set_deaths)
        res.Bind(wx.EVT_SPINCTRL, self.set_res)

    def set_name(self, event: wx.CommandEvent) -> None:
        self.data['name'] = event.GetString()
        self.parent.update()

    def set_hero(self, event: wx.CommandEvent) -> None:
        hero = event.GetString()
        self.data['current_hero'] = hero
        if hero == 'mercy':
            self.res.Enable()
            self.data['resurrects'] = self.res.GetValue()
        else:
            self.res.Disable()
            self.data['resurrects'] = None
        self.parent.update()

    def set_kills(self, event: wx.SpinEvent) -> None:
        self.data['kills'] = event.GetPosition()
        self.parent.update()

    def set_deaths(self, event: wx.SpinEvent) -> None:
        self.data['deaths'] = event.GetPosition()
        self.parent.update()

    def set_res(self, event: wx.SpinEvent) -> None:
        self.data['resurrects'] = event.GetPosition()
        self.parent.update()


class ScoreboardGui(wx.Frame):
    def __init__(self, *, callback: Optional[Callback] = None) -> None:
        wx.Frame.__init__(self, None)
        self.callback = callback
        self._data: List[Player] = []

        sizer = wx.GridSizer(2, 6, 0, 0)

        for team in range(2):
            for player in range(6):
                data = {
                    'name': f'{["Blue", "Red"][team]} {player + 1}',
                    'current_hero': 'dva',
                    'kills': 0,
                    'deaths': 0,
                    'resurrects': None
                }
                self._data.append(data)
                panel = PlayerPanel(self, data)
                sizer.Add(panel, 0, wx.EXPAND, 5)

        self.SetSizerAndFit(sizer)

        self.Center()
        self.Show()

    @classmethod
    def create(cls) -> 'ScoreboardGui':
        cls.app = wx.App()
        return cls()

    def run(self, *, with_thread: Thread) -> None:
        with_thread.start()
        self.app.MainLoop()

    @property
    def data(self) -> Team:
        return {
            'teams': {
                'blue': self._data[:6],
                'red': self._data[6:]
            }
        }

    def update(self) -> None:
        if self.callback is not None:
            self.callback(self.data)


def main() -> None:
    app = wx.App()
    ScoreboardGui(callback=print)
    app.MainLoop()


if __name__ == '__main__':
    main()
