{ lib
, runCommand
, media
, python
, glibcLocales
, zip
}:

with lib;

let

  # Create a store path that has all audio files.
  audio = let
    audioAttrs = lib.catAttrs "audio" (attrValues media);
  in runCommand "audio" {
  } ''
    mkdir -p $out
    for path in ${concatStringsSep " " audioAttrs}; do
      for f in "$path/audio/generated/*"; do
        cp -a $f $out/
      done
    done
  '';

  # Table that says how files should be named.
  rules = ./files.csv;

in {

  inherit audio rules;

  # Archive that is going to be distributed.
  archive = let
    script = ./archive.py;
  in runCommand "audio.zip" {
    buildInputs = [
      zip
      glibcLocales
      (python.withPackages(ps: [ps.pandas]))
    ];
    AUDIO="audio";
  } ''
    export LC_ALL="en_US.UTF-8"
    mkdir $AUDIO
    python ${script} "${rules}" "${audio}" "$AUDIO"
    zip -j $AUDIO -r $AUDIO/*
    mv "$AUDIO.zip" "$out"
  '';

  # Tex appendix table.
  appendix = let
    script = ./tex.py;
  in runCommand "appendix-audio.tex" {
    buildInputs = [
      glibcLocales
      (python.withPackages(ps: [ps.pandas]))
    ];
  } ''
    export LC_ALL="en_US.UTF-8"
    python ${script} "${rules}" "$out"
  '';
}
