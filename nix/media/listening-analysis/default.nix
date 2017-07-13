{ python
, runCommand
, matplotlibHook
, listening-test-tests
, listening-test-results
}:

let
 name = "listening-analysis";
in rec {

  figures = let
    kind = "figures";
  in runCommand "${name}-${kind}" {
    buildInputs = [
      (python.withPackages (ps: with ps; [ pandas seaborn ] ) )
      matplotlibHook
    ];
  } ''
    mkdir -p "$out/${kind}/generated/${name}"
    tar -xzf ${listening-test-tests} -C .
    python3 ${./figures.py} "." ${listening-test-results} "$out/${kind}/generated/${name}"
  '';

}
