{ stdenv
, fetchurl
, pandoc
, figures
, audio
, runCommand
, imagemagick
, python
}:

let
  src = fetchurl {
    url = https://github.com/hakimel/reveal.js/archive/3.5.0.tar.gz;
    sha256 = "1bfcvzz023s5kbcnzz0h9zil069x58lazrc5l58shhagw44qiiaf";
  };

  slides = ./slides.md;
  template = ./template.revealjs;
  script = ./figures.py;
  # We need PNG figures
#   figs = runCommand "figures" {
#     buildInputs = [ (python.withPackages(ps: [ps.Wand]))];
#   } ''
#     mkdir -p $out
#     python ${script} ${figures} $out
#   '';
  figs = stdenv.mkDerivation {
    name = "figures";
    src = figures;
    buildInputs = [ imagemagick ];
    buildPhase = ''
      mogrify -density 600 -format png */*/*.eps
    '';

    installPhase = ''
      mkdir -p $out
      mv generated $out/
      mv manual $out/
    '';

  };
  
in figs
  
#   
# in stdenv.mkDerivation {
#   name = "presentation.html";
#   inherit src;
# 
#   buildInputs = [ pandoc ];
# 
#   buildPhase = ''
#     ln -s ${figs} figures
#     ln -s ${audio.audio} audio
#     ln -s ${slides} slides.md
#     ln -s ${template} template.revealjs
#     
#     ls -Al figures/
#     
# 	pandoc --section-divs -t revealjs --standalone --self-contained --template=template.revealjs --slide-level=2 -o slides.html slides.md
#   '';
# 
#   installPhase = ''
#     cp slides.html $out
#   '';
# 
# 
# }
