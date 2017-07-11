{ python
, runCommand
, texlive
, fontconfig
, pkgs
, matplotlibHook
, to_wav
}:

let
 name = "turbulence-tone";
in rec {

  computations = let
    kind = "computations";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ auraliser seaborn ] ) )
      matplotlibHook
    ];
  } ''
    mkdir -p $out
    python3 ${./computations.py} $out
  '';

  figures = let
    kind = "figures";
  in runCommand "${name}-${kind}" {
    preferLocalBuild = true;
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    cp ${computations}/*.{eps,png} "$out/${kind}/generated/${name}"
  '';

  audio = let
    kind = "audio";
  in runCommand "${name}-${kind}" {
    preferLocalBuild = true;
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    cp ${computations}/*.wav "$out/${kind}/generated/${name}/"
  '';

}
