TObject *TObjArray::FindObject(const char *name) const
{
   R__COLLECTION_READ_LOCKGUARD(ROOT::gCoreMutex);

   Int_t nobjects = GetAbsLast()+1;
   for (Int_t i = 0; i < nobjects; ++i) {
      TObject *obj = fCont[i];
      if (obj && 0 == strcmp(name, obj->GetName())) return obj;
   }
   return nullptr;
}

TObject *TCollection::FindObject(const char *name) const
{
   TIter next(this);
   TObject *obj;

   while ((obj = next()))
      if (!strcmp(name, obj->GetName())) return obj;
   return nullptr;
}
