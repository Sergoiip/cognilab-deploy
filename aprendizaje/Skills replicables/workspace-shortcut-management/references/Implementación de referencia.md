# Implementación de referencia

## Descubrimiento y orden
La fuente usa KDE Plasma/KWin. Inspeccionar `XDG_CURRENT_DESKTOP`, `XDG_SESSION_TYPE`, `plasmashell --version`, `~/.config/kwinrc`, `~/.config/kglobalshortcutsrc` y los `.desktop` aplicables. Mediante `terminal`, consultar:

```text
qdbus6 --literal org.kde.KWin /VirtualDesktopManager org.freedesktop.DBus.Properties.GetAll org.kde.KWin.VirtualDesktopManager
```

En la referencia Plasma 6.7 no había método move en esa interfaz DBus, pero el API de scripting ofrecía `workspace.moveDesktop(desktopObject, zeroBasedPosition)`. Confirmarlo en `src/scripting/workspace_wrapper.h` de la versión instalada. La propuesta para otra versión requiere comprobación previa.

El script temporal toma `workspace.windowList()`, cada ID y `w.desktops.map(d => d.id)`, valida cantidad y objetivo, mueve y compara. Emitir JSON con `console.warn` y {{PREFIJO_LOG}}. Cargar con `qdbus6 org.kde.KWin /Scripting org.kde.kwin.Scripting.loadScript {{SCRIPT_PRUEBA}} {{NOMBRE_PRUEBA}}`, iniciar con `org.kde.kwin.Scripting.start`, leer orden y `journalctl --user --since '2 minutes ago' --no-pager -g {{PREFIJO_LOG}}`; después `unloadScript {{NOMBRE_PRUEBA}}`. Resolver los dos tokens locales de prueba antes de invocar.

## Atajos y lanzamiento
La implementación previa utiliza un script KWin persistente de enfocar-o-lanzar y `registerShortcut`. No se distribuye el script. Inspeccionar {{SCRIPT_EXISTENTE}} y conservar todas sus acciones, incluida cualquier acción independiente de disposición de espacios.

Si se usa QDBusRunner, la llamada `org.tubbadu.QDBusRunner /runner org.tubbadu.QDBusRunner.run` solo acredita despacho. `gtk-launch {{DESKTOP_ID}}` usa lanzadores instalados; obtener el ID y la clase real sin copiar los del equipo fuente. Descubrir metadatos con un script temporal de `workspace.windowList()`.

Consultar disponibilidad con `qdbus6 org.kde.kglobalaccel /kglobalaccel org.kde.KGlobalAccel.isGlobalShortcutAvailable {{CODIGO_TECLA}} ''`. Los modificadores Qt incluyen Meta `0x10000000` y Shift `0x02000000`; combinarlos mediante OR bit a bit con herramienta de cálculo y código de la tecla real. Leer acción mediante `org.kde.KGlobalAccel.action {{CODIGO_TECLA}}`; invocar mediante `qdbus6 org.kde.kglobalaccel /component/kwin org.kde.kglobalaccel.Component.invokeShortcut '{{ID_ACCION}}'` y verificar ventana.

Recargar con unload/load/start del nombre real del script. Para un visor GTK lanzado por servicio sin DISPLAY/XAUTHORITY, verificar `systemctl --user show-environment` sin divulgar los valores sensibles. `systemd-run --user --collect --quiet {{INTERPRETE}} {{VISOR}}` mantiene el proceso real como principal. No usar `gtk-launch` como proceso principal transitorio: su salida temprana puede provocar limpieza del hijo. No fijar un archivo xauth de la sesión fuente. Para reproducir una falla X11 de GTK, usar `GDK_BACKEND=x11`: probar `Gtk.init_check` sin este backend puede pasar por Wayland y engañar.

## Captura y nota
Para Spectacle 6.7, la referencia identifica grupo `GuiConfig`, clave `quitAfterSaveCopyExport=true` de `spectaclerc`. Confirmar en `src/Gui/SettingsDialog/spectacle.kcfg` y `src/SpectacleCore.cpp` del código KDE/spectacle en la rama compatible; `willQuit` combina UserAction y la clave. Cerrar solo instancia de inspección ociosa mediante `qdbus6 org.kde.Spectacle /MainApplication org.qtproject.Qt.QCoreApplication.quit`. Cambiar con `kwriteconfig6 --file spectaclerc --group GuiConfig --key quitAfterSaveCopyExport --type bool true`, leer archivo exacto; `kreadconfig6 --type bool` puede señalar verdad en exit status. Esto verifica configuración, no copia/pegado.

Si el visor GTK requiere botón de actualización, activarlo y leer todo el árbol accesible. Si un wrapper rechaza `element_index`, usar píxeles desde captura reciente y límites locales explícitos, no offsets supuestos. Ningún atajo, nombre de ventana o visor privado de la fuente se exporta.

Origen: notas técnicas desidentificadas de una implementación de referencia; compatibilidad sujeta a comprobación local.
