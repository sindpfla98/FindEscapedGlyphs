# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
import os

class FindEscapedGlyphs(GeneralPlugin):
	window = objc.IBOutlet()
	MinX_tf = objc.IBOutlet()
	MinY_tf = objc.IBOutlet()
	MaxX_tf = objc.IBOutlet()
	MaxY_tf = objc.IBOutlet()
	result_tf = objc.IBOutlet()

	selectedGlyphs_ckb = objc.IBOutlet()

	@objc.python_method
	def settings(self):

		self.name = Glyphs.localize({
			'en': 'Find Escaped Glyphs',
			'ko': '벗어난 글립 찾기',
			})
		self.loadNib('IBdialog', __file__)
		return

	@objc.python_method
	def start(self):
		try:
			try:
				newMenuItem = NSMenuItem(self.name, self.showWindow_)
				Glyphs.menu[GLYPH_MENU].append(newMenuItem)
			except:
				mainMenu = Glyphs.mainMenu()
				s = objc.selector(self.showWindow_, signature='v@:@')
				newMenuItem = NSMenuItem.alloc().initWithTitle_action_(self.name, s)
				newMenuItem.setTarget_(self)
				mainMenu.itemWithTag_(3).submenu().addItem_(newMenuItem)
		except:
			pass

	@objc.python_method
	def showWindow_(self, sender):
		self.window.makeKeyAndOrderFront_(self)

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

	@objc.IBAction
	def setApplyButtonClicked_(self, sender):
		MinX = self.MinX_tf.integerValue()
		MinY = self.MinY_tf.integerValue()
		MaxX = self.MaxX_tf.integerValue()
		MaxY = self.MaxY_tf.integerValue()
		selected = self.selectedGlyphs_ckb.state()

		if selected:
			for layer in Glyphs.font.selectedLayers:
				result = checkLayer(self, layer, MinX, MinY, MaxX, MaxY, result)

		else:
			for glyph in Glyphs.font.glyphs:
				for layer in glyph.layers:
					if layer.master == Glyphs.font.selectedFontMaster:
						result = checkLayer(self, layer, MinX, MinY, MaxX, MaxY, result)
		
		result += ('\n' + 'Done')
		self.result_tf.setString_(result)
				

	@objc.IBAction
	def setCancleButtonClicked_(self, sender):
		self.window.close()

def checkLayer(self, layer, MinX, MinY, MaxX, MaxY, result):
	print_result = False
	bounds = layer.bounds
	if bounds.origin.x < MinX:
		print_result = True
	if bounds.origin.y < MinY:
		print_result = True
	if bounds.origin.x + bounds.size.width > MaxX:
		print_result = True
	if bounds.origin.y + bounds.size.height > MaxY:
		print_result = True
	if print_result:
		result += ('\n' + layer.parent.name)
		
	return result
