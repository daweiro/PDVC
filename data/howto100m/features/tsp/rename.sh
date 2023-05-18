for file in *npy
do
   mv "$file" "${file/.mp4/}"
done
