from osu import Mods


hddtfl = Mods.Hidden | Mods.DoubleTime | Mods.Flashlight
ezhr = Mods.Easy | Mods.HardRock
rx = Mods.Relax

print(ezhr.is_compatible_combination())
print(list(hddtfl))
print(hddtfl.to_readable_string())
print(rx.is_compatible_with(Mods.NoFail))
print(rx.is_compatible_with(Mods.Hidden))
print(rx.get_incompatible_mods())
