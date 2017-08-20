{ lib
, runCommand
, media
}:

with lib;

let
  figs = catAttrs "figures" (attrValues media);
  manual = ../../data/report/figures/manual;
in runCommand "figures" { } ''
  # prepare
  mkdir -p $out
  mkdir $out/generated
  cp -rL ${manual} $out/manual
#   cp $map figures/manual/figure_trajectory.png

  # fill it up
  pushd $out/generated
  for path in ${concatStringsSep " " figs}; do
    for f in "$path/figures/generated/*"; do
      cp -rL $f .
    done
  done
  popd

  # and move it out
  #mv figures $out

''
