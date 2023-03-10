#!/bin/bash

if [ -z "$(ls -A incoming)" ]; then
        exit 0
else
        for pdf in incoming/*.pdf
        do
                echo "*** Start processing $pdf ***"
                docker run --rm -i jbarlow83/ocrmypdf -l deu - - <"$pdf" >"ocr/$(basename -- "$pdf")"
                mv "$pdf" "archive/$(basename -- "$pdf")"
                echo "*** End processing $pdf ***"

        done
fi
