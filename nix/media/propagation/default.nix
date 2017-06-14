{ python
, runCommand
, texlive
, fontconfig
, pkgs
, matplotlibHook
}:

let
 name = "propagation";
in rec {

  computations = let
    kind = "computations";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ acoustics auraliser h5store ] ) )
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
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./figures.py} ${computations} "$out/${kind}/generated/${name}"
  '';

  figures-slides = let
    kind = "figures-slides";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ acoustics h5store matplotlib] ) )
      matplotlibHook
    ];
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./figures-slides.py} ${computations} "$out/${kind}/generated/${name}"
  '';


  audio = let
    kind = "audio";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ acoustics h5store ] ) )
    ];
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./audio.py} ${computations} "$out/${kind}/generated/${name}"
  '';

}
