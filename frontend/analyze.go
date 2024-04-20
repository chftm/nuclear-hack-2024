package main

import (
	"math/rand"
	"mime/multipart"
	"strconv"
)

type Result struct {
	Emotion string
}

func analyze(_ multipart.File) (Result, string) {
	return Result{Emotion: "happy"}, strconv.Itoa(rand.Int())
}

func fetch(_ string) Result {
	return Result{Emotion: "sad"}
}
