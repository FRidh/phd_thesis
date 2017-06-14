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
  XELATEX="xelatex -halt-on-error";
in stdenv.mkDerivation {
  name = "thesis-announcement.pdf";
  src = thesis-source;

  sourceRoot = "${thesis-source.name}/report2";

  buildInputs = [ latex biber ghostscript ];

  buildPhase = ''
    ${XELATEX} ${filename}.tex #&& biber ${filename}.bcf && biber ${filename}.bcf && ${XELATEX} ${filename}.tex
  '';

  installPhase = ''
    mv ${filename}.pdf $out
  '';
}
