package main

import (
	"context"
	"fmt"
	"os"

	"github.com/Xenia101/ytdl"
)

func main() {
	vid, err := ytdl.GetVideoInfo(context.Background(), "https://www.youtube.com/watch?v=WkVvG4QTO9M")
	if err != nil {
		fmt.Println(err)
		return
	}

	file, _ := os.Create(vid.Title + ".mp4")
	defer file.Close()
	ytdl.DefaultClient.Download(context.Background(), vid, vid.Formats.Worst(ytdl.FormatResolutionKey)[0], file)
}
