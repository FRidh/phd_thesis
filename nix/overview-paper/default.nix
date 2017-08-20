{ stdenv
, runCommand
, references
, media
, audio
, figures
, latex
, biber
, ghostscript
, makeFontsCache
, python
, which
}:


with stdenv.lib;

let
  pythonEnv = python.withPackages(ps: [ps.pygments]);

#   figures = let
#     figs = catAttrs "figures" (attrValues media);
#     map = ../data/report/figures/manual/auralisation-paper/figure_trajectory.png;
#   in runCommand "figures" { } ''
#     # prepare
#     mkdir figures
#     mkdir figures/generated
#     mkdir figures/manual
#     cp ${map} figures/manual/figure_trajectory.png
#     pushd figures/generated
#
#     # fill it up
#     for path in ${concatStringsSep " " figs}; do
#       for f in "$path/figures/generated/*"; do
#         cp $f .
#       done
#     done
#     popd
#
#     # and move it out
#     mv figures $out
#   '';

  src = ./paper.tex;
#   figures =
  XELATEX="xelatex -halt-on-error -shell-escape";
  fontsConf = makeFontsCache {
    fontDirectories = [
      "${ghostscript}/share/ghostscript/fonts"
    ];
  };
  filename = "paper";

in stdenv.mkDerivation {
  name = "2017_overview.pdf";
  unpackPhase = "true";

  buildInputs = [ latex biber ghostscript pythonEnv which ];

  buildPhase = ''
    ln -s ${src} ${filename}.tex
    ln -s ${figures} figures
    ln -s ${references} library.bib

    ls -Al

    export FONTCONFIG_FILE=${fontsConf}
    ${XELATEX} ${filename}.tex && biber ${filename}.bcf && biber ${filename}.bcf && ${XELATEX} ${filename}.tex
  '';


  installPhase = ''
    cp "${filename}.pdf" "$out"
  '';



}
