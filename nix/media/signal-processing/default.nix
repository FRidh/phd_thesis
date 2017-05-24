{ python
, runCommand
, matplotlibHook
}:

rec {

  figures = let
    kind = "figures";
    name = "signal-processing";
  in runCommand "${name}-${kind}" {
    buildInputs = [
    (python.withPackages (ps: with ps; [ acoustics matplotlib seaborn ] ) )
    matplotlibHook
    ];
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./figures.py} "$out/${kind}/generated/${name}"
  '';

}
