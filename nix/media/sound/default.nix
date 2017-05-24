{ python
, runCommand
, matplotlibHook
}:

rec {

  figures = let
    kind = "figures";
    name = "sound";
  in runCommand "${name}-${kind}" {
    buildInputs = [
    (python.withPackages (ps: with ps; [ acoustics matplotlib seaborn ] ) )
    matplotlibHook
    ];
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    python3 ${./figures.py} "$out/${kind}/generated/${name}"
  '';

#   figures = create_figure {
#     name = "sound";
#     deps = [ (python.withPackages (ps: with ps; [ acoustics matplotlib seaborn ] ) ) ];
#     script = ${./figures};
#   };

}
