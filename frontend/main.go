package main

import (
	"fmt"
	"net/http"

	"chftm.dev/nuclear-hack-2024/views"
	"github.com/a-h/templ"
)

func main() {
	mux := http.NewServeMux()

	index := views.Index()
	mux.HandleFunc("GET /{$}", func(w http.ResponseWriter, r *http.Request) {
		serveHtmxPage(r, w, index)
	})

	mux.HandleFunc("POST /upload", func(w http.ResponseWriter, r *http.Request) {
		file, _, err := r.FormFile("file")
		if err != nil {
			panic(err) // TODO
		}
		defer file.Close()

		result, id := analyze(file)

		w.Header().Add("HX-Push-Url", fmt.Sprint("/result/", id))
		serveHtmxPage(r, w, views.Result(result.Emotion))
	})

	mux.HandleFunc("GET /result/{id}", func(w http.ResponseWriter, r *http.Request) {
		result := fetch(r.PathValue("id"))
		serveHtmxPage(r, w, views.Result(result.Emotion))
	})

	http.ListenAndServe(":8080", mux)
}

func serveHtmxPage(r *http.Request, w http.ResponseWriter, component templ.Component) {
	if r.Header.Get("HX-Request") != "true" {
		component = views.Page(component)
	}
	component.Render(r.Context(), w)
}
