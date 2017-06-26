{ python
, runCommand
, matplotlibHook
, to_wav
}:

let
 name = "recording-to-auralisation";
in rec {

  computations = ../../../data/media/recording-to-auralisation;

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

  audio = let
    kind = "audio";
    source = "${computations}";
    target = "${kind}/generated/${name}";
  in to_wav "${name}-${kind}" source target;

}
