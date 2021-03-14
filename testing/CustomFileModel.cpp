Qlist * getFileList (FileItem * parent)
{
    Qlist * result = new QList();
    // FileItem - class of the file element, I will describe it later.
    QString path = parent-> getFilePath ();
    QTextCodec * localeCodec = QTextCodec :: codecForLocale ();
    
    fs :: path full_path (fs :: initial_path());
    full_path = fs :: system_complete (fs :: path (localeCodec-> fromUnicode (path) .append ('\ 0'). data ())); // Get the full path to the directory in the boost view
    try // In case of a ban on reading
    {
    if (fs :: exists (full_path) && fs :: is_directory (full_path)) // Check for the existence and whether it really is a directory, otherwise it doesn't matter
    {
        fs :: directory_iterator end_iter;
    
        for (fs :: directory_iterator dir_itr (full_path); dir_itr! = end_iter; ++ dir_itr)
        {
        FileItem * fileInfo = 0;
        try // In case of a ban on reading
        {
            fileInfo = new FileItem (localeCodec-> toUnicode (dir_itr-> path (). string (). c_str ()),
                        fs :: is_directory (dir_itr-> status ()),
                        parent
                        (! fs :: is_directory (dir_itr-> status ())? fs :: file_size (dir_itr-> path ()): 0),
                        QDateTime :: fromTime_t (last_write_time (dir_itr-> path ()))); // Create a new tree element
    
    
            result-> append (fileInfo); // and add it to the result
        }
        catch (const std :: exception & ex)
        {
            delete fileInfo; // If something went wrong, delete it
        }
        }
    }
    }
    catch (const std :: exception & ex)
    {
    }
    return result;
}

    class FileItem
    {
    public:
      FileItem (QString filePath, bool fileIsDir, FileItem * parent = 0, int size = 0, QDateTime date = QDateTime :: currentDateTime ());
     
      void setFilePath (QString what);
      void setFileSize (int what) {size = what; }
      void setFileDateTime (QDateTime what) {date = what; }
      void setIsDir (bool what) {fileIsDir = what; }
      void setChildren (QList* what);
     
      QString getFilePath () const {return filePath; }
      QString getFileName () const;
      QString getFileSize () const; // In the "human-readable" view
      int getFileSizeInBytes () const {return size; } // In bytes
      QDateTime getFileDateTime () const {return date; }
      bool isDir () const {return fileIsDir; }
      Qlist* getChildren () {return children; }
      void addChild (FileItem * item);
      int childCount () const {return children-> count (); }
      int row () const; // Returns its parent list number
      FileItem * parent () {return itemParent; }
      void setFetched (bool what) {fetched = what; }
      bool getFetched () const {return fetched; }
     
    private:
      void setParent (FileItem * parent) {itemParent = parent; } // In case the parent is not known during creation
     
      QString filePath;
      QString fileName;
      int size;
      QDateTime date;
      bool fileIsDir;
      FileItem * itemParent;
      Qlist * children;
      bool fetched; // Have we already downloaded the children?
     
    };

        FileItem :: FileItem (QString filePath, bool fileIsDir, FileItem * parent, int size, QDateTime date)
    {
      this-> filePath = filePath;
      if (filePath.isEmpty ())
        fileName = "";
      else
      {
    #ifdef Q_OS_WIN // Do Not Forget That Windows Has Disks
        if (filePath.size () == 3 && filePath.at (1) == QLatin1Char (':'))
        {
          fileName = filePath;
          fileName.chop (1);
        }
        else
        {
          QStringList fileParts = filePath.split ("/");
          fileName = fileParts.last ();
        }
    #else // but in * nix they are not
        QStringList fileParts = filePath.split ("/");
        fileName = fileParts.last ();
    #endif
      }
      this-> fileIsDir = fileIsDir;
      this-> size = size;
      this-> date = date;
      this-> itemParent = parent;
      this-> children = new QList();
      if (fileIsDir &&! filePath.isEmpty ())
      {
        fetched = false; // We have not yet loaded the children.
        addChild (new FileItem ("dummy", false, this)); // Terrible muck, but without this, the widget will not sculpt you pluses for daddies,
        // because it will assume that they are empty.
        // By the way, the minus of this approach is that we don’t know if the folder is really empty
        // and sculpt the pluses to everything,
        // unfortunately kicking every child directory for “not empty” is too expensive an undertaking.
      }
    }

    class FileItemModel: public QAbstractItemModel
    {
    public:
      enum Columns // Four Obvious Columns We Need
      {
        NameColumn = 0,
        SizeColumn,
        TypeColumn,
        Datecolumn
      };
     
      FileItemModel ();
      ~ FileItemModel ();
     
      QVariant data (const QModelIndex & index, int role = Qt :: DisplayRole) const; // Important virtual function, its definition is required
                                            // responsible for displaying all the information in the tree
      Qt :: ItemFlags flags (const QModelIndex & index) const; // (virtual, required)
      QVariant headerData (int section, Qt :: Orientation orientation, int role = Qt :: DisplayRole) const; // Responsible for column headings (virtual, required)
      QModelIndex index (int row, int column, const QModelIndex & parent = QModelIndex ()) const; // Returns the index of the element (virtual, required)
      QModelIndex parent (const QModelIndex & index) const; // Returns the parent index (virtual, required)
      int rowCount (const QModelIndex & parent = QModelIndex ()) const; // (virtual, required)
      int columnCount (const QModelIndex & parent = QModelIndex ()) const; // (virtual, required)
      FileItem * item (QModelIndex index) const {return static_cast(index.internalPointer ()); } // Returns the item by index
      FileItem * getRootItem () {return rootItem; }
      bool hasChildren (const QModelIndex & index) const {return index.isValid ()? item (index) -> childCount (): true; }
      bool canFetchMore (const QModelIndex & index) const {return index.isValid ()? ! item (index) -> getFetched (): true; }
      void fetchMore (const QModelIndex & index); // It is executed when the plus sign (or minus sign) is pressed (virtual, mandatory)
      void refresh () {emit layoutChanged (); }
     
    private:
      FileItem * rootItem;
      static const int ColumnCount = 4; // Columns are always 4
      QFileIconProvider iconProvider; // Standard icons of disks, files and folders
     
    protected:
      void readDir (FileItem * item); // Loads children
     
    };

        FileItemModel :: FileItemModel ()
    {
      lastSortColumn = 0;
      lastSortOrder = Qt :: AscendingOrder;
    #ifdef Q_OS_WIN // How many wonderful discoveries we have ...
      rootItem = new FileItem ("", true); // And all because in windows there is no root as such
      QFileInfoList drives = QDir :: drives (); // But there are wheels
      for (QFileInfoList :: iterator driveIt = drives.begin (); driveIt! = drives.end (); ++ driveIt) // Here we create them
      {
        FileItem * drive = new FileItem ((* driveIt) .absolutePath (), true);
        rootItem-> addChild (drive);
      }
    #else
      QString path = QDir :: rootPath ();
      rootItem = new FileItem (path, true);
      readDir (rootItem); // read the contents of the root immediately
    #endif
    }
     
    void FileItemModel :: readDir (FileItem * item)
    {
      item-> setChildren (getFileList (item)); // Get the children and immediately bind them to the ancestor
      // Sort call omitted here
    }
     
    void FileItemModel :: fetchMore (const QModelIndex & index)
    {
      if (index.isValid () &&! item (index) -> getFetched ()) // If you have never downloaded children yet, then download.
      {
        readDir (item (index));
        item (index) -> setFetched (true);
        refresh ();
      }
    }