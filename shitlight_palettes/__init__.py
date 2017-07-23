from palettable import wesanderson
import random



class ShitPaletteSet:
	palettes = []
	preview = []

	@classmethod
	def get_random_palette(cls):
		""" Returns a random palette. A palette might include a color sequence or related colors.
		If you just want a color, use get_random_color(). """
		return random.choice(cls.palettes)

	@classmethod
	def get_random_color(cls):
		""" Returns a random color from the set. 
		Will always use the primary color, if this set contains palettes."""
		if type(cls.palettes[0])==ShitPalette:
			return cls.get_random_palette().get_primary()
		else:
			return cls.get_random_palette()

	@classmethod
	def generate_preview(cls):
		mapping = []
		if cls.preview:
			for n,c in enumerate(preview):
				mapping.append((str(cls.__name__)+"_%d" %n, "", "", "", "", "#%1x%1x%1x" % tuple((int(v)//16 for v in c))))
		else:
			if type(cls.palettes[0])==ShitPalette:
				for n,c in enumerate(cls.palettes[0:4]):
					mapping.append((str(cls.__name__)+"_%d" %n, "", "", "", "", "#%1x%1x%1x" % tuple((int(v)//16 for v in c.get_primary()))))
			else:
				for n,c in enumerate(cls.palettes[0:4]):
					mapping.append((str(cls.__name__)+"_%d" %n, "", "", "", "", "#%1x%1x%1x" % tuple((int(v)//16 for v in c))))
		return mapping

		
	@classmethod
	def __len__(cls):
		return len(cls.palettes)

	@classmethod
	def __iter__(cls):
		return cls.palettes

	@classmethod
	def __getitem__(cls,key):
		return cls.palettes[key]


class ShitPalette:
	pass




class Zissou_5(ShitPaletteSet):
	palettes = wesanderson.Zissou_5.colors

class Moonrise7_5(ShitPaletteSet):
	palettes = wesanderson.Moonrise7_5.colors

class TestFarben(ShitPaletteSet):
	palettes = [(255,255,255),(255,0,0),(0,0,255),(0,255,0)]	



palettes = [ ("Zissou 5", Zissou_5), ("Moonrise 7 5", Moonrise7_5),("Test Farben",TestFarben)]

fallback = TestFarben