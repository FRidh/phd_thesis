{ lib
, runCommand
, media

}:

with lib;

let
  audio = lib.catAttrs "audio" (attrValues media);
in runCommand "audio" {
} ''
  mkdir -p $out
  for path in ${concatStringsSep " " audio}; do
    for f in "$path/audio/generated/*"; do
      cp -a $f $out/
    done
  done
''
