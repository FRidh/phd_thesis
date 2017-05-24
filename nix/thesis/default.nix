{ stdenv
, runCommand
, latex
, biber
, media
, references
, ghostscript
}:

with stdenv.lib;

let
  # List of derivations that have figures
  figures = catAttrs "figures" (attrValues media);
#   figures = listToAttrs ( mapAttrs' (k:v: {name=k; value=( getAttr "figures" v );} )   (filterAttrs (k:v: hasAttr "figures" v) media) );
#   figures = let
#     filtered = (filterAttrs (k: v: (hasAttr "figures" v)) media);
#   in  mapAttrsToList (k: v: "${k} ${toString v.figures}") filtered ;
#   args = mapAttrsToList (k: v: "${k} ${v}" ) figures;
  filename = "report";

in stdenv.mkDerivation {
  name = "thesis";
  src = ./../../data;

  buildInputs = [ latex biber ghostscript ];

  buildPhase = ''
    # Link all the figures we have in the figures folder
    pushd figures/generated
    for path in ${concatStringsSep " " figures}; do
      echo "Linking path $path"
      for f in "$path/figures/generated/*"; do
        echo $f
        ln -s $f
      done
    done
    popd
    ls -Al figures

    # Build the report
    pushd report
    ln -s ${references} library.bib # We need the references

    xelatex ${filename}.tex && biber ${filename}.bcf && biber ${filename}.bcf && xelatex ${filename}.tex
    popd
  '';

  installPhase = ''
    mv report/report.pdf $out
  '';
}
