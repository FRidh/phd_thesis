{ pkgs
, python
, runCommand
, lib
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

  # Take a directory with .hdf5 files and convert to audio.
  # - `name` is the name of the derivation
  # - `source` is the absolute path to directory containing .hdf5 files.
  # - `target` is the path relative to $out.
  to_wav = name: source: target:
    runCommand name {
      buildInputs = [
        (python.withPackages (ps: with ps; [ acoustics h5store ] ) )
      ];
      preferLocalBuild = true;
    } ''
      mkdir -p "$out/${target}"
      python3 ${./audio.py} "${source}" "$out/${target}"
    '';

#   create_audio_figure = {name, source, target, script }:
#     let
#       kind = "figures";
#       pythonEnv = (python.withPackages (ps: with ps; [ acoustics h5store matplotlib] ) );
#     in runCommand "${name}-${kind}" {
#       buildInputs = [ pythonEnv lib.matplotlibHook ];
#     } ''
#       mkdir -p "$out/${kind}/generated/${name}"
#       python3 ${script} "$out/${kind}/generated/${name}"
#     '';

#     figures-common-rc = {
#       "figure.figsize" = [ 6.0 3.0 ];
#       "font.size" = 10.0;
#       "text.usetex" = true;
#     };

}
