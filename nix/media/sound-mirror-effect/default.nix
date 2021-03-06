{ python
, runCommand
, texlive
, fontconfig
, pkgs
, matplotlibHook
, to_wav
}:

let
 name = "sound-mirror-effect";
in rec {

  computations = let
    kind = "computations";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ common_simulation ] ) )
    ];
  } ''
    mkdir -p $out
    python3 ${./computations.py} $out
  '';

  figures = let
    kind = "figures";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ acoustics h5store matplotlib] ) )
      matplotlibHook
    ];
    preferLocalBuild = true;
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./figures.py} ${computations} "$out/${kind}/generated/${name}"
  '';

#   figures-slides = let
#     kind = "figures-slides";
#   in runCommand "${name}-${kind}" {
#     buildInputs = [
#       (python.withPackages (ps: with ps; [ acoustics h5store matplotlib] ) )
#       matplotlibHook
#     ];
#   } ''
#     mkdir -p "$out/${kind}/generated/${name}"
#     python3 ${./figures-slides.py} ${computations} "$out/${kind}/generated/${name}"
#   '';

  audio = let
    kind = "audio";
    source = "${computations}";
    target = "${kind}/generated/${name}";
  in to_wav "${name}-${kind}" source target;

}
