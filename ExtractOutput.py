
class ExtractOutput:
    def __init__(self):
        self.file_name = "crapOP"
        self.keywords = ['Claim:', 'Status:', 'Origins:', 'Sources:']

    def run_main(self):
        
        keyword = ""
        cat_val_list = []
        val_list = []

        for line in open(self.file_name).readlines():

            line = line and line.strip()
            if not line:continue            

            if line.startswith("Claim:") or keyword == "Claim":
                if line.startswith("Status:"):
                    claim_val = " ".join(val_list)
                    cat_val_list.append(claim_val)   
                    val_list = []
                    val_list.append(line)
                    keyword = "Status"
                    continue
 
                keyword = "Claim"    
                val_list.append(line)
            
            elif line.startswith("Status:") or keyword == "Status":
                if line.startswith("Origins:"):
                    status_val = " ".join(val_list)
                    cat_val_list.append(status_val)
                    val_list = []
                    val_list.append(line)
                    keyword = "Origin"
                    continue

                keyword = "Status"
                val_list.append(line)
                
            elif line.startswith("Origins:") or keyword == "Origin":
                if line.startswith("Sources:"):
                    import pdb;pdb.set_trace()
                    origin_val = " ".join(val_list)
                    cat_val_list.append(origin_val)
                    val_list = []
                    val_list.append(line)
                    keyword = "Sources"
                    continue    

                keyword = "Origin"
                val_list.append(line)

            elif line.startswith("Sources:") or keyword == "Sources":
                val_list.append(line)


        if keyword == "Sources":
            source_val = " ".join(val_list)
            cat_val_list.append(source_val)
            val_list = []
            
        print cat_val_list

if __name__ == "__main__":
    eo_obj = ExtractOutput()
    eo_obj.run_main()
