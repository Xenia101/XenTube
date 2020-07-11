package gui

import (
	"fyne.io/fyne"
	"fyne.io/fyne/app"
	"fyne.io/fyne/widget"
)

func Window() {
	app := app.New()
	w := app.NewWindow("Test Window")

	text1 := widget.NewLabel("topleft")
	text2 := widget.NewLabel("Middle Label")
	text3 := widget.NewLabel("bottomright")

	w.SetContent(fyne.NewContainerWithLayout(&diagonal{}, text1, text2, text3))

	w.ShowAndRun()
}
