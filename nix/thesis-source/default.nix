{ stdenv
, runCommand
, references
, media
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

  src = ./../../data/report;

in stdenv.mkDerivation {
  name = "thesis-source";
  inherit src;

  buildPhase = ''
    # Link all the figures we have in the figures folder
    pushd figures/generated
    for path in ${concatStringsSep " " figures}; do
      for f in "$path/figures/generated/*"; do
        ln -s $f
      done
    done
    popd

    # We need the references
    pushd report
    ln -s ${references} library.bib
    popd
  '';

  installPhase = ''
    mkdir -p $out
    mv * $out
  '';

  preferLocalBuild = true;
}

# in runCommand "thesis-source" {
#   preferLocalBuild = true;
# } ''
#   cp -r ${src}/* .
#   chmod -R 0744 .
#
#   ls -Al
#   ls -Al figures
#
#   # Link all the figures we have in the figures folder
#   pushd figures/generated
#   for path in ${concatStringsSep " " figures}; do
#     for f in "$path/figures/generated/*"; do
#       ln -s $f
#     done
#   done
#   popd
#
#   # We need the references
#   pushd report
#   ln -s ${references} library.bib
#   popd
#
#   # Copy everything to $out
#   mkdir -p $out
#   mv * $out
# ''
