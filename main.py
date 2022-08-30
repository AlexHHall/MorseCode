from WindowSetup import *

app = App()
Menu = MenuBar(app, "translator", app)
Page = TranslatorPage(app)
app.mainloop()
