import PySimpleGUI as sg
import pkgutil
import importlib
import sys
import io
import pydoc

class App:
	def __init__(self):
		self.title='MyDoc'
		self.theme_name='Dark Amber'
		sg.theme(self.theme_name)
		self.rng=True
		self.data='''A easy to use documentation reader.'''
		self.attributes=tuple()
		self.doc=Doc()

	def set_layout(self):
		self.input_box=sg.Input(key='INP',size=(35,None))
		self.dropdown=sg.DropDown(self.attributes,default_value='Available methods',key='DDN',size=(42,None))
		self.button=sg.Button('Search',key='SRC')
		self.checkbox=sg.Checkbox('Detailed Documentation',key='CBX')
		self.text_box=sg.Multiline(self.data,key='TB',disabled=True,size=(60,20))
		self.layout=[
		[self.input_box,self.button],
		[self.dropdown],
		[self.checkbox],
		[self.text_box]]

	def main(self):
		self.set_layout()
		self.window=sg.Window(self.title,self.layout)
		while self.rng:
			event,values=self.window.read()
			if event==sg.WIN_CLOSED:
				self.rng=False
			elif event=='SRC':
				self.data,self.attributes=self.doc.get_method(values['INP'],not values['CBX'])
				self.text_box.update(self.data)
				self.dropdown.update(values=self.attributes)


class Doc:
	def __init__(self):
		pass


	def get_method(self,arg,is_detailed):
		if is_detailed:
			method_list=arg.split('.')
			try:
				module=importlib.import_module(method_list[0])
				data,attributes=self.get_doc(module,method_list,1)
			except:
				module=importlib.import_module('builtins')
				data,attributes=self.get_doc(module,method_list,0)
			return data,attributes
		else:
			f=io.StringIO()
			pydoc.doc(arg, output=f)
			f.seek(0)
			data=f.read()
			return data,tuple()


	def get_doc(self,module,module_list,n):
		if n>=len(module_list):
			try:
				data,attributes=module.__doc__,sorted(tuple(module.__dict__.keys(),))
				if data:
					return data,attributes
				else:
					return 'No documentation found!',attributes
			except AttributeError as error:
				print(error)
				return module.__doc__,tuple()

		else:
			try:
				module=getattr(module,module_list[n])
				data,attributes=self.get_doc(module,module_list,n+1)
			except:
				data,attributes='Unknown Module\\Class\\Function\\Sub-module!!!\nNo such module\\class\\function\\sub-module was found.',tuple()
		return data,attributes



if __name__ == '__main__':
	app=App()
	app.main()