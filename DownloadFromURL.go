package main

import (
	"context"
	"fmt"
	"os"

	"github.com/Xenia101/ytdl"
)

func DownloadFromURL(URL string) {
	vid, err := ytdl.GetVideoInfo(context.Background(), URL)
	if err != nil {
		fmt.Println(err)
		return
	}

	file, _ := os.Create(vid.Title + ".mp3")
	defer file.Close()
	ytdl.DefaultClient.Download(
		context.Background(),
		vid,
		vid.Formats.Worst(ytdl.FormatResolutionKey)[0],
		file)
}
