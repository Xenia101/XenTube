package main

import (
	"context"
	"os"

	"github.com/rylio/ytdl"
)

func download() {
	ctx := context.Background()
	client := ytdl.DefaultClient

	videoInfo, err := client.GetVideoInfo(ctx, "https://www.youtube.com/watch?v=uR-Gk-nAICE")
	if err != nil {
		panic(err)
	}

	file, err := os.Create("storage/" + videoInfo.Title + ".mp3")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	err = client.Download(ctx, videoInfo, videoInfo.Formats[0], file)
	if err != nil {
		panic(err)
	}
}
