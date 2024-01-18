@echo off

rem Process each .pcap file in the current directory
for %%i in (*.pcap) do (
  set input_file=%%~fi
  set file_name=%%~ni
  set output_file=%file_name%.csv
  
  echo Processing: %file_name%
  
  tshark -r "%input_file%" -T fields -E header=y -E separator=, -E quote=d -E occurrence=f ^
    -e ip.src -e ip.dst -e frame.protocols -e frame.len -e frame.time_delta_displayed ^
    -e tcp.dstport -e udp.dstport -e ip.proto -e frame.time_relative > "%output_file%"
  
  echo Done: %file_name%
)

echo All files processed.
