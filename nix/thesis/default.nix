{ stdenv
, latex
, biber
, ghostscript
, makeFontsCache
# Contents
, thesis-source
, python
, which
}:

with stdenv.lib;

let
  filename = "main";
  # -shell-escape for `minted` package
  XELATEX="xelatex -halt-on-error -shell-escape";
  fontsConf = makeFontsCache {
    fontDirectories = [
      "${ghostscript}/share/ghostscript/fonts"
    ];
  };
  pythonEnv = python.withPackages(ps: [ps.pygments]);
#   XELATEX="pdflatex";
in stdenv.mkDerivation {
  name = "thesis.pdf";
  src = thesis-source;

  sourceRoot = "${thesis-source.name}/report2";

  # pythonEnv and which are needed for the `minted` latex package
  buildInputs = [ latex biber ghostscript pythonEnv which ];

  buildPhase = ''
    export FONTCONFIG_FILE=${fontsConf}
    ${XELATEX} ${filename}.tex && biber ${filename}.bcf && biber ${filename}.bcf && ${XELATEX} ${filename}.tex
  '';

  installPhase = ''
    mv ${filename}.pdf $out
  '';
}
