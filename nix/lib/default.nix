{ pkgs
}:

{
  # A hook for matplotlib for drawing text with ghostscript.
  # Note that you need to add matplotlib yourself.
  matplotlibHook = let
    fontsConf = pkgs.makeFontsCache {
      fontDirectories = [
        "${pkgs.ghostscript}/share/ghostscript/fonts"
      ];
    };
  in pkgs.makeSetupHook {
    deps = with pkgs; [ fontconfig texlive.combined.scheme-full ghostscript ];
    substitutions = { inherit fontsConf; };
  } ./matplotlib.sh;


#   create_figure = { name, deps, script }:
#     let
#       kind = "figures";
#     in runCommand "${name}-${kind}" {
#       buildInputs = [ matplotlibHook ] + deps;
#     ];
#   } ''
#     mkdir -p "$out/${kind}/generated/${name}"
#     python3 ${script} "$out/${kind}/generated/${name}"
#   '';
}
