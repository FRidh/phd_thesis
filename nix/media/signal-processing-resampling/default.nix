{ python
, runCommand
, texlive
, fontconfig
, pkgs
, matplotlibHook
, to_wav
}:

let
 name = "signal-processing-resampling";
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
      (python.withPackages (ps: with ps; [ acoustics h5store matplotlib ] ) )
      matplotlibHook
    ];
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./figures.py} ${computations} "$out/${kind}/generated/${name}"
  '';

  audio = let
    kind = "audio";
    source = "${computations}";
    target = "${kind}/generated/${name}";
  in to_wav "${name}-${kind}" source target;

}
