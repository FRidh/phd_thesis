{ stdenv
, latex
, biber
, ghostscript
# Contents
, thesis-source
}:

with stdenv.lib;

let
  filename = "main-for-defence-announcement";
#   LATEX="xelatex -halt-on-error";
  LATEX="pdflatex";
in stdenv.mkDerivation {
  name = "thesis-announcement.pdf";
  src = thesis-source;

  sourceRoot = "${thesis-source.name}/report";

  buildInputs = [ latex biber ghostscript ];

  buildPhase = ''
    ${LATEX} ${filename}.tex
  '';

  installPhase = ''
    mv ${filename}.pdf $out
  '';
}
