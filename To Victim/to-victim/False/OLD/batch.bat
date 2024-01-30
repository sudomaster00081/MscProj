@echo off
setlocal enabledelayedexpansion

rem Process each .pcap file in the current directory
for %%i in (*.pcap) do (
  set input_file=%%~fi
  set file_name=%%~ni
  set output_file=!file_name!.csv
  set temp_file=!file_name!.temp

  echo Processing: !file_name!

  tshark -r "!input_file!" -T fields -E header=n -E separator=, -E quote=d -E occurrence=f ^
    -e ip.src -e ip.dst -e frame.protocols -e frame.len -e frame.time_delta_displayed ^
    -e tcp.dstport -e udp.dstport -e ip.proto -e frame.time_relative > "!temp_file!"

  (
    echo ip.src,ip.dst,frame.protocols,frame.len,frame.time_delta_displayed,tcp.dstport,udp.dstport,ip.proto,frame.time_relative
  ) > "!output_file!"

  for /f "tokens=1-9 delims=," %%a in ('type "!temp_file!"') do (
    set /A len=%%d, time_delta=%%e, dstport=%%f, proto=%%h, time_relative=%%i

    echo %%a,%%b,%%c,!len!,!time_delta!,!dstport!,%%g,!proto!,!time_relative! >> "!output_file!"
  )

  del "!temp_file!"

  echo Done: !file_name!
)

echo All files processed.
endlocal
